from IGoogleDrive import IGoogleDrive
from files.Google import *
from googleapiclient.errors import HttpError
from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime, timedelta
import pytz
from files.constatns import *

CLIENT_SECRET_FILE='credentials.json'
API_NEAME = 'drive'
API_VERSION='v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

class ClassGoogleDrive(IGoogleDrive):


    
    def Create_Service(self): 
        service = Create_Service(CLIENT_SECRET_FILE,API_NEAME,API_VERSION,SCOPES)
        return service
    

    def copy_public_file_to_my_drive(self,service, public_file_url): #יעתיק ויחזיר את האיי די החדש
        public_file_id = self.extract_file_id_from_public_url(public_file_url)

        #cheak size of the file
        size = self.get_file_size(service, public_file_id) 
        if size is None:
            print("file size not found")
            return 
        if not self.is_enough_space(service,size):
            print("there is no enough space in the google account")
            return


        try:
            folder_name = datetime.now().strftime("%Y-%m-%d")
            folder_id = self.get_or_create_folder(service, folder_name)

            # Get the original file's metadata
            original_file_metadata = service.files().get(fileId=public_file_id, fields='name,description').execute()
            original_file_name = original_file_metadata['name']
            original_file_description = original_file_metadata.get('description', '')

        # Set the metadata for the copied file
            copied_file_metadata = {
                'name': original_file_name,
                'description': original_file_description,
                'parents': [folder_id]
        }

            copied_file = service.files().copy(
                fileId=public_file_id,
                body=copied_file_metadata
            ).execute()

            copied_file_id = copied_file['id']
            print("The public file has been copied to your drive.")
            return copied_file_id
        except HttpError as error:
            copied_file = None
            if error.resp.status == 403:
                print("You don't have permission to copy this file.")
                return response_type.NOT_ENOUGH_PERMISSIONS
            else:
                print(f"An error occurred: {error}")


    def share_file_with_email(self,service, file_id, email):
        try:
            permissions = {
                'type': 'user',
                'role': 'reader',  # or 'writer' 
                'emailAddress': email
            }

            service.permissions().create(
                fileId=file_id,
                body=permissions,
                fields='id'
            ).execute()
            print(f"File ID {file_id} has been shared with {email}.")

        except HttpError as error:
           if error.resp.status == 403:
            print(f"An error occurred: {error}")




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
        
    
    def get_or_create_folder(self, service, folder_name):
        query = f"mimeType='application/vnd.google-apps.folder' and trashed = false and name='{folder_name}'"
        results = service.files().list(q=query, fields="files(id)").execute()
        folders = results.get("files", [])

        if not folders:
            metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=metadata, fields="id").execute()
            folder_id = folder["id"]
        else:
            folder_id = folders[0]["id"]

        return folder_id

        
    
    

    def get_file_size(self,service, file_id):
        try:
            #Getting information about the file
            file_metadata = service.files().get(fileId=file_id, fields="size").execute()

           
            file_size = file_metadata.get("size")
            
            if file_size:
                return int(file_size)
            else:
                print("We could not find the file")
                return None
        except HttpError as error:
            print(f"get_file_size: {error}")
            return None
        

    def is_enough_space(self,service, file_size):
        try:
            # Receiving information about the storage of the account
            storage_info = service.about().get(fields="storageQuota").execute()

            # Finding the amount of free space in the account
            total_space = int(storage_info['storageQuota']['limit'])
            used_space = int(storage_info['storageQuota']['usage'])

            free_space = total_space - used_space

            # Checking if there is enough free space
            if file_size <= free_space:
                return True
            else:
                return False
        except HttpError as error:
            print(f"is_enough_space: {error}")
            return False
        

    def delete_old_folders(self,service, hours):
        try:
            #Finding all folders in the main Google Drive
            query = "mimeType='application/vnd.google-apps.folder' and trashed = false and 'root' in parents"
            results = service.files().list(q=query, fields="nextPageToken, files(id, createdTime, name)").execute()
            folders = results.get("files", [])

            # Setting the time before the folders are deleted
            delete_before = datetime.now(pytz.utc) - timedelta(hours=hours)

            for folder in folders:
                created_time = datetime.fromisoformat(folder["createdTime"][:-1]).replace(tzinfo=pytz.utc)
                if created_time < delete_before:
                    # Deleting the folder and all its contents
                    service.files().delete(fileId=folder["id"]).execute()
                    print(f"Deleted folder: {folder['name']}")

        except HttpError as error:
            print(f"An error occurred: {error}")

                

            