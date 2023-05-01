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
            urls_emails = mails.get_list_of_driveUrl_and_emails(gmail_service)
            print(urls_emails)

            for google_drive_url,email_account,message_id in urls_emails:
                my_private_new_id = google_drive.copy_public_file_to_my_drive(drive_service,google_drive_url)

                if my_private_new_id == response_type.NOT_ENOUGH_PERMISSIONS: 
                    mails.send_reply(gmail_service, message_id, email_account,my_private_new_id)
                    continue

                google_drive.share_file_with_email(drive_service,my_private_new_id,email_account)
            time.sleep(60)
        except Exception as e:
            print(e)

        
    


if __name__ == "__main__":
    main()