from abc import ABC, abstractmethod

class IGoogleDrive(ABC):

    @abstractmethod
    def Create_Service(self): 
        pass

    @abstractmethod
    def copy_public_file_to_my_drive(self,service, public_file_url): #יעתיק ויחזיר את האיי די החדש
        pass

    @abstractmethod
    def share_file_with_email(self,service, file_id, email):
        pass

    @abstractmethod
    def delete_old_folders(self,service, hours):
        pass

    @abstractmethod
    def convert_file_ids_to_urls(self,files):
        pass

    @abstractmethod
    def convert_folder_ids_to_urls(self,folders):
        pass

    @abstractmethod
    def get_list_of_folders_in_folder(self,service, folder_id):
        pass

    @abstractmethod
    def get_list_of_files_in_folder(self,service, folder_id):
        pass