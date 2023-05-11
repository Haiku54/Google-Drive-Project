from google_drive.IGoogleDrive import *
from gmail.IGmail import *
import time
from google_drive.GoogleDrive import *
from gmail.Gmail import *
from files.constatns import *

def main():
    google_drive: IGoogleDrive = ClassGoogleDrive()
    mails: IGmail = gmailClass()
    data_base: IDataBase = MySQLDataBase()

    drive_service = google_drive.Create_Service()
    time.sleep(2)
    gmail_service = mails.Create_Service()


    while True:
        try:
            
            requestId_messageId = mails.get_list_of_requesrIDs_and_massageIDs(gmail_service)
            print(requestId_messageId)

            for request_id,message_id in requestId_messageId:
                response_id = google_drive.copy_public_file_to_my_drive(drive_service,request_id)

                # If the file didn't copied to my drive
                if isinstance(response_id, response_type):

                    # If the folder is requested
                    if response_id == response_type.FOLDER_EXISTS:
                        #get the files in this folder 
                        all_files_and_names = google_drive.get_list_of_files_in_folder(drive_service, google_drive. data_base.get_requsted_folderID(request_id))
                        #get the folders in this folder 
                        all_folders_and_names = google_drive.get_list_of_folders_in_folder(drive_service,data_base.get_requsted_folderID(request_id))

                        #convert all ids to urls
                        all_urls_and_names = google_drive.convert_folder_ids_to_urls(all_folders_and_names) +google_drive.convert_file_ids_to_urls(all_files_and_names) 
                        mails.send_reply(gmail_service, message_id,request_id ,response_id,all_urls_and_names)
                    #send sutible reply
                    else:
                        mails.send_reply(gmail_service, message_id,request_id ,response_id)
                    continue

                google_drive.share_file_with_email(drive_service,response_id,request_id)
            time.sleep(30)
        except Exception as e:
            print(e)

        
    


if __name__ == "__main__":
    main()