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

    