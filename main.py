from IGoogleDrive import IGoogleDrive
from IGmail import IGmail
import time
from GoogleDrive import ClassGoogleDrive
from Gmail import gmailClass
from constatns import response_type

def main():
    google_drive: IGoogleDrive = ClassGoogleDrive()
    mails: IGmail = gmailClass()

    drive_service = google_drive.Create_Service()
    time.sleep(2)
    gmail_service = mails.Create_Service()


    while True:
        urls_emails = mails.get_list_of_driveUrl_and_emails(gmail_service)
        print(urls_emails)

        for google_drive_url,email_account,message_id in urls_emails:
            my_private_new_id = google_drive.copy_public_file_to_my_drive(drive_service,google_drive_url)

            if my_private_new_id == response_type.NOT_ENOUGH_PERMISSIONS: #אין הרשאה
                mails.send_reply(gmail_service, message_id, email_account,my_private_new_id)
                continue #להגיב למשתמש

            google_drive.share_file_with_email(drive_service,my_private_new_id,email_account)
        time.sleep(60)
    


if __name__ == "__main__":
    main()