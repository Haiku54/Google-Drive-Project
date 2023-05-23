from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
import re
import pytz
from googleapiclient.errors import HttpError
from files.constatns import *
from data_base.dataBase import *
from files.Google import *
from files.singlton import Singleton
from datetime import datetime


CLIENT_SECRET_FILE='credentials.json'
API_NEAME = 'drive'
API_VERSION='v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

class ClassGoogleDrive(Singleton):

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.service = self.__Create_Service()
        self.data_base = MySQLDataBase()

    
    def __Create_Service(self): 
        service = Create_Service(CLIENT_SECRET_FILE,API_NEAME,API_VERSION,SCOPES)
        return service
    

    def copy_public_file_to_my_drive(self, request_id): 
        """
        Copies a file from a public link to the user's Google Drive and returns the new file ID.

        Parameters:
        self (AIProgrammingAssistant): the AIProgrammingAssistant object itself.
        service (googleapiclient.discovery.Resource): the Google Drive service being used to copy the file.
        request_id (str): the ID of the request for copying the file from the database.

        Returns:
        str: The ID of the copied file if it was copied successfully.
        If the requested file is not found in public link, it returns "FILE_NOT_FOUND".
        If there isn't enough space in the user's Google account after deleting the oldest file, InsufficientSpaceException is raised.
        If the copy fails due to lack of permissions or any other error, it returns an error message describing the problem.
        """
        
        public_file_id = self.data_base.get_requestFile_id_by_request_id(request_id)

        #Checking if the requested file is already in my Google Drive and if so, return the id of the file in the drive
        file_id_from_myDrive = self.data_base.get_returned_file_id_active(public_file_id) 
        if file_id_from_myDrive is not None:
            return file_id_from_myDrive


        #if sender uploaded 0.5 GB file in the last 2 hours
        email_sender = self.data_base.get_email_by_request_id(request_id)
        if self.data_base.is_user_uploaded_half_GB_last_2_hours(email_sender):
            return response_type.ALREADY_SENT_LAST
        
        # if the file is a shortcut, get the original file ID
        file = self.service.files().get(fileId=public_file_id,supportsAllDrives=True).execute()
        
        #if the file is a shortcut, then public_file_id_shortcut is the shortcut file id else it is the same as public_file_id
        public_file_id_shortcut = public_file_id
        if file['mimeType'] == 'application/vnd.google-apps.shortcut':
            print('This file is a shortcut.')
            public_file_id = self.get_original_file_id(public_file_id_shortcut)
        
        #cheak size of the file
        size = self.get_file_size(public_file_id) 

        if size is None:
            print("file size not found")
            return 
        if size == "Error 404":
            return response_type.FILE_NOT_FOUND
        
        #Inserting the file size into the request table
        self.data_base.update_file_size_in_requested_files(public_file_id_shortcut,size)
        
        if not self.is_enough_space(size):
            #try to delete the oldest file one day before
            self.delete_oldest_file(self.service,24)
            if not self.is_enough_space(size):
                raise InsufficientSpaceException("Error: not enough space in google account aftr deleting the oldest file")
            print("deleted the oldest file succeeded")

        try:
            folder_name = datetime.now().strftime("%Y-%m-%d")
            folder_id = self.get_or_create_folder( folder_name)

            # Get the original file's metadata
            original_file_metadata = self.service.files().get(fileId=public_file_id, fields='name,description',supportsAllDrives=True).execute()
            original_file_name = original_file_metadata['name']
            original_file_description = original_file_metadata.get('description', '')

        # Set the metadata for the copied file
            copied_file_metadata = {
                'name': original_file_name,
                'description': original_file_description,
                'parents': [folder_id]
        }

            copied_file = self.service.files().copy(
                fileId=public_file_id,
                body=copied_file_metadata,
                supportsAllDrives=True
            ).execute()

            copied_file_id = copied_file['id']
            print("The public file has been copied to your drive.")

            # Update copied file value
            self.data_base.update_is_copied_to_true(request_id)
            # Insert into returned files table.
            self.data_base.insert_returned_files(copied_file_id,public_file_id_shortcut)
            #Insert into a table of currently active files in my Google Drive
            self.data_base.insert_activeFiles(copied_file_id,public_file_id_shortcut)
            
            return copied_file_id
        except HttpError as error:
            copied_file = None
            if error.resp.status == 403:
                print("You don't have permission to copy this file.")
                return response_type.NOT_ENOUGH_PERMISSIONS
            else:
                print(f"An error occurred: {error}")


    def check_file_or_folder(self,request_id):
        # Request the file's metadata
        file_id = self.data_base.get_requestFile_id_by_request_id(request_id)
        file_metadata = self.service.files().get(fileId=file_id,supportsAllDrives=True).execute()

        if file_metadata['mimeType'] == 'application/vnd.google-apps.folder':
            # The file is a folder, update the database and return the corresponding string
            self.data_base.update_is_folder(request_id, 1)
            return 'Folder'
        else:
            self.data_base.update_is_folder(request_id, 0)
            return 'File'


    def share_file_with_email(self, file_id, request_id):
        """
        Shares a file with a user by their email address.

        parameters:
        self (AIProgrammingAssistant): the AIProgrammingAssistant object itself.
        service (googleapiclient.discovery.Resource): the Google Drive service being used to share the file.
        file_id (str): the ID of the file to share.
        request_id (str): the ID of the request for sharing the file from the database.
        """
        try:
            # Get the email address of the user to share the file with
            email = self.data_base.get_email_by_request_id(request_id)
            permissions = {
                'type': 'user',
                'role': 'reader',  # or 'writer' 
                'emailAddress': email
            }

            # Insert new permission
            self.service.permissions().create(
                fileId=file_id,
                body=permissions,
                fields='id'
            ).execute()

            #Inserting the returned ID into the request table
            self.data_base.update_request_with_returned_file(request_id,file_id)
            print(f"File ID {file_id} has been shared with {email}.")

        except HttpError as error:
           if error.resp.status == 403:
            print(f"An error occurred: {error}")

           
    def get_or_create_folder(self, folder_name):
        """
        Gets or creates a folder in the user's Google Drive.
        parameters:
        self (AIProgrammingAssistant): the AIProgrammingAssistant object itself.
        service (googleapiclient.discovery.Resource): the Google Drive service being used to create the folder.
        folder_name (str): the name of the folder to create.
        
        Returns:
        str: The ID of the folder.
        """

        query = f"mimeType='application/vnd.google-apps.folder' and trashed = false and name='{folder_name}'"
        results = self.service.files().list(q=query, fields="files(id)").execute()
        folders = results.get("files", [])

        # If the folder doesn't exist, create it
        if not folders:
            metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.service.files().create(body=metadata, fields="id").execute()
            # Get the folder ID
            folder_id = folder["id"]
        else:
            folder_id = folders[0]["id"]

        return folder_id    
    
    

    def get_file_size(self, file_id):
        try:
            #Getting information about the file
            file_metadata = self.service.files().get(fileId=file_id, fields="size",supportsAllDrives=True).execute()

           
            file_size = file_metadata.get("size")
            
            if file_size:
                return int(file_size)
            else:
                print("We could not find the file")
                return None
        except HttpError as error:
            if error.resp.status == 404:
                print("get_file_size: File not found (404)")
                return "Error 404"
            else:
                print(f"get_file_size: {error}")
            return None

        

    def is_enough_space(self, file_size):
        try:
            # Receiving information about the storage of the account
            storage_info = self.service.about().get(fields="storageQuota").execute()

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
        

    def delete_old_folders(self, hours):
        try:
            #Finding all folders in the main Google Drive
            query = "mimeType='application/vnd.google-apps.folder' and trashed = false and 'root' in parents"
            results = self.service.files().list(q=query, fields="nextPageToken, files(id, createdTime, name)").execute()
            folders = results.get("files", [])

            # Setting the time before the folders are deleted
            delete_before = datetime.now(pytz.utc) - timedelta(hours=hours)

            for folder in folders:
                created_time = datetime.fromisoformat(folder["createdTime"][:-1]).replace(tzinfo=pytz.utc)
                if created_time < delete_before:
                    list_of_files = self.get_list_of_files_in_folder(self.service, folder["id"])

                    # Deleting the folder and all its contents
                    self.service.files().delete(fileId=folder["id"]).execute()

                    # Deleting the files from the active_files table
                    self.data_base.delete_files_from_active_files(list_of_files)

                    print(f"Deleted folder: {folder['name']}")

        except HttpError as error:
            print(f"An error occurred: {error}")

    
    def get_list_of_files_in_folder(self, folder_id):
        try:
            query = f"'{folder_id}' in parents and trashed = false"
            results = self.service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
            files = results.get("files", [])
            return files
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
        

    def get_list_of_folders_in_folder(self, folder_id):
        try:
            query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed = false"
            results = self.service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
            folders = results.get("files", [])
            return folders
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
        

    def convert_file_ids_to_urls(self,files):
        urls = []
        for file in files:
            file_id = file['id']
            name = file['name']
            file_url = f"https://drive.google.com/file/d/{file_id}/view"
            urls.append((file_url,name))
        return urls
    

    def convert_folder_ids_to_urls(self,folders):
        urls = []
        for folder in folders:
            folder_id = folder['id']
            name = folder['name']
            folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
            urls.append((folder_url,name))
        return urls
    

    def get_original_file_id(self,shortcut_file_id):
        # Build the Drive API service
    

        # Get the shortcut file
        request = self.service.files().get(fileId=shortcut_file_id, fields='shortcutDetails',supportsAllDrives=True)
        file = request.execute()

        # The ID of the original file is in the 'targetId' field of the 'shortcutDetails' field
        original_file_id = file['shortcutDetails']['targetId']

        print (original_file_id)
        return original_file_id


        

                

            