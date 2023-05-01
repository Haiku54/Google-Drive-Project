import re
import base64
from files.constatns import *
from email.utils import parseaddr
from IGmail import IGmail
from googleapiclient.errors import HttpError
from files.Google import Create_Service
from googleapiclient.discovery import build
from google.oauth2 import service_account
from email.mime.text import MIMEText
from data_base.IDataBase import *
from data_base.dataBase import *
from datetime import datetime

CLIENT_SECRET_FILE='credentials.json'
API_NEAME = 'gmail'
API_VERSION='v1'
SCOPES = ['https://mail.google.com/']

class gmailClass(IGmail):
    data_base: IDataBase = SQLDataBase()
    """def __init__(self):
          self.data_base"""
          
       
    def Create_Service(self): 
        service = Create_Service(CLIENT_SECRET_FILE,API_NEAME,API_VERSION,SCOPES)
        return service

    
    def get_list_of_driveUrl_and_emails(self,service): 
        try:
            unread_msgs = service.users().messages().list(
                  userId='me',
                  labelIds=['INBOX'],
                  q='is:unread'
                ).execute()
            messages = unread_msgs.get('messages', [])

            google_drive_links = []

            for message in messages:
                # Mark message as read
                service.users().messages().modify(
                    userId='me', 
                    id=message['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()
                
                msg = service.users().messages().get(
                      userId='me',
                      id=message['id']
                    ).execute()
                msg_body = msg['snippet']
                sender_email,sender_name = self.get_sender_email(msg)
                if not sender_email:
                    print(f"An error occurred: there is no sender")
                    return 

                
                # Regular expression to find Google Drive links
                drive_link_pattern = re.compile(r'https://drive\.google\.com/[^ \n]+')

                drive_links = drive_link_pattern.findall(msg_body)

                if drive_links:
                    for link in drive_links:
                        if not self.data_base.is_RequestedFiles_in_table(self.extract_file_id_from_public_url(link)):
                            self.data_base.insert_requested_files(self.extract_file_id_from_public_url(link),None)
                        dataBase_id = self.data_base.insert_requests(sender_email,sender_name,self.extract_file_id_from_public_url(link), None,datetime.now(),None)

                        #The link to the file, the email account of the sender of the message and the ID of the message
                        google_drive_links.append([link, sender_email,message['id']]) 

                

            return google_drive_links

        except HttpError as error:
                print(f"An error occurred: {error}")
                return None
        
    

    def get_sender_email(self,msg):
        for header in msg['payload']['headers']:
            if header['name'] == 'From':
                sender_name, sender_email = parseaddr(header['value'])
                return sender_email,sender_name
        return None
    


    def send_reply(self,service, msg_id, to_email, response:response_type):
        if response == response_type.NOT_ENOUGH_PERMISSIONS:
            reply_body = NOT_ENOUGH_PERMISSIONS_MESSAGE
        if reply_body:

                # Create MIMEText object with the reply body
            message = MIMEText(reply_body)
            message['To'] = to_email
            message['In-Reply-To'] = msg_id
            message['References'] = msg_id
            message['Subject'] = 'קובץ הגוגל דרייב שביקשת בשיתוף פרטי'

            # Encode the MIMEText object and associate it with the original message thread
            create_message = {
                'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8'),
                'threadId': msg_id
            }

            # Send the reply message 
            try:
                send_message = service.users().messages().send(
                 userId='me',
                 body=create_message
                 ).execute()
                print(F'sent message to {to_email} Message Id: {send_message["id"]}')
            except HttpError as error:
                print(F'An error occurred: {error}')
                send_message = None

            return send_message
        

    def extract_file_id_from_public_url(self,url):
    # Regular expression pattern to match Google Drive file IDs
        file_id_pattern = r'(?:file\/d\/|\/d\/|id=)([-\w]+)'
    
        match = re.search(file_id_pattern, url)
    
        if match:
             file_id = match.group(1)
             print(file_id)
             return file_id
        else:
             print("Could not find a valid file ID in the given URL.")
             return None



