from abc import ABC, abstractmethod

class IDataBase(ABC):

    @abstractmethod
    def Insert_Requested_Files(self,FileID,FileSize): 
        pass

    @abstractmethod
    def Insert_Returned_Files(self,FileID,RequestedFileID): 
        pass
    
    @abstractmethod
    def Insert_Requests(self,Email,Name,RequestedFileID,ReturnedFileID,RequestDate,IsCopied): 
        pass

    @abstractmethod
    def Insert_ActiveFiles(self,ReturnedFileID,RequestedFileID): 
        pass

    