from google_drive.IGoogleDrive import *
from gmail.IGmail import *
import time
from google_drive.GoogleDrive import *
from gmail.Gmail import *
from files.constatns import *

def main():
    google_drive: IGoogleDrive = ClassGoogleDrive()
    mails: IGmail = gmailClass()

    drive_service = google_drive.Create_Service()
    time.sleep(2)
    gmail_service = mails.Create_Service()


    while True:
        try:
            requestId_messageId = mails.get_list_of_driveUrl_and_emails(gmail_service)
            print(requestId_messageId)

            for request_id,message_id in requestId_messageId:
                my_private_new_id = google_drive.copy_public_file_to_my_drive(drive_service,request_id)

                if isinstance(my_private_new_id, response_type):
                    mails.send_reply(gmail_service, message_id,request_id ,my_private_new_id)
                    continue

                google_drive.share_file_with_email(drive_service,my_private_new_id,request_id)
            time.sleep(60)
        except Exception as e:
            print(e)

        
    


if __name__ == "__main__":
    main()