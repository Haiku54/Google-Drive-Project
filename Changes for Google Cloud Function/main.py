
import time
from google_drive.GoogleDrive import *
from gmail.Gmail import *
from files.constatns import *

def main(*args, **kwargs):
    mails = GmailService() 
    time.sleep(0.5)
    google_drive = ClassGoogleDrive()
    data_base = MySQLDataBase()

    try:
        requestId_messageId = mails.get_list_of_requesrIDs_and_massageIDs()
        print(requestId_messageId)
        for request_id,message_id in requestId_messageId:
            file_type = google_drive.check_file_or_folder(request_id)
            if(file_type == "Folder"):
                    response_id = response_type.FOLDER_EXISTS
            else:
                response_id = google_drive.copy_public_file_to_my_drive(request_id)

            # If the file didn't copied to my drive
            if isinstance(response_id, response_type):
                # If the folder is requested
                if response_id == response_type.FOLDER_EXISTS:
                    #get the files in this folder 
                    all_files_and_names = google_drive.get_list_of_files_in_folder(google_drive. data_base.get_requestFile_id_by_request_id(request_id))
                    #get the folders in this folder 
                    all_folders_and_names = google_drive.get_list_of_folders_in_folder(data_base.get_requestFile_id_by_request_id(request_id))
                    #convert all ids to urls
                    all_urls_and_names = google_drive.convert_folder_ids_to_urls(all_folders_and_names) +google_drive.convert_file_ids_to_urls(all_files_and_names) 
                    mails.send_reply(message_id,request_id ,response_id,all_urls_and_names)
                #send sutible reply
                else:
                    mails.send_reply( message_id,request_id ,response_id)
                continue
            google_drive.share_file_with_email(response_id,request_id)

            # code that may raise an exception
    except Exception as e:
        if hasattr(e, 'resp') and e.resp.status == 404:
            if 'message_id' in locals() and 'request_id' in locals():
                mails.send_reply(message_id, request_id, response_type.FILE_NOT_FOUND)
            else:
                # handle the case where message_id and request_id are not defined
                print('Error: message_id and request_id are not defined')
        else:
            # handle other exceptions
            print('Error:', e)
    
    data_base.close_connection()

