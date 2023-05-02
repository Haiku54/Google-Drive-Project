from abc import ABC, abstractmethod

class IDataBase(ABC):

    @abstractmethod
    def insert_requested_files(self,FileID,FileSize): 
        pass

    @abstractmethod
    def insert_returned_files(self,FileID,RequestedFileID): 
        pass
    
    @abstractmethod
    def insert_requests(self,Email,Name,RequestedFileID,ReturnedFileID,RequestDate,IsCopied): 
        pass

    @abstractmethod
    def insert_activeFiles(self,ReturnedFileID,RequestedFileID): 
        pass
    
    @abstractmethod
    def is_RequestedFiles_in_table(self, file_id):
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def get_email_by_request_id(self, request_id):
        pass
    
    @abstractmethod
    def get_requestFile_id_by_request_id(self, request_id):
        pass
    
    @abstractmethod
    def update_is_copied_to_true(self, request_id):
        pass

    @abstractmethod
    def update_file_size_in_requested_files(self, file_id, file_size):
        pass

    @abstractmethod
    def update_request_with_returned_file(self, request_id, returned_file_id):
        pass

    @abstractmethod
    def insert_into_active_files(self, requested_file_id, returned_file_id):
        pass
    

    