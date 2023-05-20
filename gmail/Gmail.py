import re
import base64
from files.constatns import *
from email.utils import parseaddr
from googleapiclient.errors import HttpError
from files.Google import Create_Service
from files.singlton import Singleton
from googleapiclient.discovery import build
from google.oauth2 import service_account
from email.mime.text import MIMEText
from data_base.dataBase import *
from datetime import datetime
import googleapiclient.discovery
from bs4 import BeautifulSoup

CLIENT_SECRET_FILE='credentials.json'
API_NAME = 'gmail'
API_VERSION='v1'
SCOPES = ['https://mail.google.com/']

class GmailService(Singleton):
    def __init__(self):
            if hasattr(self, "_initialized"):
                return
            
            self.service = self.__create_service()
            self.data_base = MySQLDataBase()
            self._initialized = True


    def  __create_service(self): 
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        return service

    
    def get_list_of_requesrIDs_and_massageIDs(self): 
        
        try:
            unread_msgs = self.service.users().messages().list(
                  userId='me',
                  labelIds=['INBOX'],
                  q='is:unread'
                ).execute()
            messages = unread_msgs.get('messages', [])

            # A list of tuples (request_id, message_id)
            requestIDs_messageIDs = [] 

            for message in messages:
                # Mark message as read
                self.service.users().messages().modify(
                    userId='me', 
                    id=message['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()
                
                msg = self.service.users().messages().get(
                      userId='me',
                      id=message['id']
                    ).execute()
                #msg_body = msg['snippet']
                sender_email,sender_name = self.get_sender_email(msg)
                if not sender_email:
                    print(f"An error occurred: there is no sender")
                    return 
                
                #temporary inspection. Only authorized emails can receive service
                if not self.data_base.is_email_authorized(sender_email):
                    raise PermissionError(f"Access denied for email: {sender_email}")


                drive_file_links, drive_folder_links = self.get_drive_links_from_msg('me',message['id'])
                if drive_file_links:
                    file_id = drive_file_links[0]['id'] # only one file link is allowed
                    if not self.data_base.is_RequestedFiles_in_table(file_id):
                        self.data_base.insert_requested_files(file_id,None)
                    request_id = self.data_base.insert_requests(sender_email,sender_name,file_id, None,datetime.now(),None,None)

                    #The link to the file, the email account of the sender of the message and the ID of the message
                    requestIDs_messageIDs.append((request_id,message['id'])) 
                
                elif drive_folder_links:
                    folder_id = drive_folder_links[0]['id'] # only one folder link is allowed
                    request_id = self.data_base.insert_requests(sender_email,sender_name,None, None,datetime.now(),None,folder_id)
                    requestIDs_messageIDs.append((request_id,message['id']))


            return requestIDs_messageIDs

        except HttpError as error:
                print(f"An error in get_list_of_requesrIDs_and_massageIDs: {error}")
                return None

                
                # Regular expression to find Google Drive links
                """drive_link_pattern = re.compile(r'https://drive\.google\.com/(file/d/[^/]+/view|u/\d+/open\?id=[^ \n]+)[^ \n]*')


                drive_links = drive_link_pattern.findall(msg_body)

                if drive_links:
                    link = drive_links[0]
                    if not self.data_base.is_RequestedFiles_in_table(self.extract_file_id_from_public_url(link)):
                        self.data_base.insert_requested_files(self.extract_file_id_from_public_url(link),None)
                    request_id = self.data_base.insert_requests(sender_email,sender_name,self.extract_file_id_from_public_url(link), None,datetime.now(),None,None)

                    #The link to the file, the email account of the sender of the message and the ID of the message
                    requestIDs_messageIDs.append((request_id,message['id'])) 

                else:
                #if this is folder link of google drive
                    folder_link_pattern = re.compile(r'https://drive\.google\.com/drive(?:/u/\d+)?/folders/[^ \n]+')
                    folder_links = folder_link_pattern.findall(msg_body)

                    #if there is folder link
                    if folder_links:
                        link = folder_links[0]
                        request_id = self.data_base.insert_requests(sender_email,sender_name,None, None,datetime.now(),None,self.extract_folder_id_from_url(link))
                        requestIDs_messageIDs.append((request_id,message['id']))

                        
                    else:
                        #continue
                        
                        msg = self.service.users().messages().get(userId='me', id=message['id']).execute()

                        links = []

                        if 'payload' in msg:
                            payload = msg['payload']
                            for part in payload.get('parts', []):
                                mime_type = part['mimeType']
                                body = part['body']
                                data = body['data']
                                if mime_type == "text/plain":
                                    # Using urlsafe base64 decoding
                                    text = base64.urlsafe_b64decode(data).decode()
                                    # Find URLs using a regular expression
                                    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                                    urls = re.findall(url_pattern, text)
                                    links.extend(urls)
                                if mime_type == "text/html":
                                    # Using urlsafe base64 decoding
                                    text = base64.urlsafe_b64decode(data).decode()
                                    soup = BeautifulSoup(text, 'html.parser')
                                    for link in soup.find_all('a', href=True):
                                        links.append(link['href'])
                        if links:
                            #find google drive link in all links
                            for link in links:
                                link = drive_link_pattern.findall(link)
                                if link:
                                    link = link[0]
                                    if not self.data_base.is_RequestedFiles_in_table(self.extract_file_id_from_public_url(link)):
                                        self.data_base.insert_requested_files(self.extract_file_id_from_public_url(link),None)
                                    request_id = self.data_base.insert_requests(sender_email,sender_name,self.extract_file_id_from_public_url(link), None,datetime.now(),None,None)
                                    requestIDs_messageIDs.append((request_id,message['id'])) 
                                    break"""

                          




          
        

        

    def get_sender_email(self,msg):
        for header in msg['payload']['headers']:
            if header['name'] == 'From':
                sender_name, sender_email = parseaddr(header['value'])
                return sender_email,sender_name
        return None
        
    


    def send_reply(self, msg_id, request_id, response:response_type,all_urls=None):
        '''
        Sends a reply to the sender of the message with the given ID.
        The reply body is determined by the response type.
        param: service - the Gmail API service object
        param: msg_id - the ID of the message to reply to
        param: request_id - the ID of the request associated with the message
        param: response - the response type
        return: the sent message object
        '''
        
        if response == response_type.NOT_ENOUGH_PERMISSIONS:
            reply_body = NOT_ENOUGH_PERMISSIONS_MESSAGE
        elif response == response_type.FILE_NOT_FOUND:
            reply_body = FILE_NOT_FOUND_MESSAGE
        elif response == response_type.ALREADY_SENT_LAST:
            reply_body = ALREADY_SENT_LAST_MESSAGE
        elif response == response_type.FOLDER_EXISTS:
            #send all url files and their name
            reply_body = FOLDER_EXISTS_MESSAGE+"\n\n"
            for url, file_name in all_urls:
                reply_body += f"{file_name}\n{url}\n\n"

        if reply_body:
            to_email = self.data_base.get_email_by_request_id(request_id)

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
                send_message = self.service.users().messages().send(
                 userId='me',
                 body=create_message
                 ).execute()
                print(F'sent message to {to_email} Message Id: {send_message["id"]}')
            except HttpError as error:
                print(F'An error occurred: {error}')
                send_message = None

            return send_message
        

    def extract_file_id_from_public_url(self, url):
        # Regular expression pattern to match Google Drive file IDs
        file_id_pattern = r'(?:file\/d\/|\/d\/|id=)([-\w]+)'

        # Try to match the regular pattern
        match = re.search(file_id_pattern, url)

        if match:
            file_id = match.group(1)
            print(file_id)
            return file_id
        else:
            # Try to match the pattern with "/u/0/open?id="
            file_id_pattern = r'(?<=id=)([-\w]+)'
            match = re.search(file_id_pattern, url)
            if match:
                file_id = match.group(1)
                print(file_id)
                return file_id
            else:
                print("Could not find a valid file ID in the given URL.")
                return None

        
    
    def extract_folder_id_from_url(self, url):
        folder_id_pattern = r'(?:/folders/|/u/\d+/folders/)([\w-]+)'
        match = re.search(folder_id_pattern, url)
        if match:
            folder_id = match.group(1)
            return folder_id
        else:
            return None
        


    
    def get_drive_links_from_msg(self, user_id, msg_id):
        '''
        Extracts Google Drive links from the message with the given ID.
        param: user_id - the ID of the user's Gmail account
        param: msg_id - the ID of the message to extract links from
        return: a list of Google Drive file links and a list of Google Drive folder links
        '''

        try:
            msg = self.service.users().messages().get(userId=user_id, id=msg_id).execute()

            links = []
            drive_file_links = []
            drive_folder_links = []

            if 'payload' in msg:
                payload = msg['payload']
                for part in payload.get('parts', []):
                    mime_type = part['mimeType']
                    body = part['body']
                    data = body['data']
                    if mime_type in ["text/plain", "text/html"]:
                        # Using urlsafe base64 decoding
                        text = base64.urlsafe_b64decode(data).decode()

                        if mime_type == "text/plain":
                            # Find URLs using a regular expression
                            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                            urls = re.findall(url_pattern, text)
                            links.extend(urls)
                        else:
                            soup = BeautifulSoup(text, 'html.parser')
                            for link in soup.find_all('a', href=True):
                                links.append(link['href'])

            # Find Google Drive links from the list of all links
            for link in links:
                # Regex patterns for Google Drive file and folder URLs
                file_pattern = r'https://drive.google.com/file/d/([a-zA-Z0-9_-]+)/view'
                folder_pattern = r'https://drive.google.com/drive/folders/([a-zA-Z0-9_-]+)'
                file_match = re.search(file_pattern, link)
                folder_match = re.search(folder_pattern, link)
                if file_match:
                    drive_file_links.append({'link': link, 'id': file_match.group(1)})
                elif folder_match:
                    drive_folder_links.append({'link': link, 'id': folder_match.group(1)})

            return drive_file_links, drive_folder_links

        except HttpError as error:
            print(f'An error occurred: {error}')


    # Instantiate a service object using your credentials
    # file_links, folder_links = get_drive_links(service, 'me', 'message_id')

    # Approach the returned data like this:
    # for file_info in file_links:
    #     print(f'Google Drive File Link: {file_info["link"]}, ID: {file_info["id"]}')
    # for folder_info in folder_links:
    #     print(f'Google Drive Folder Link: {folder_info["link"]}, ID: {folder_info["id"]}')


