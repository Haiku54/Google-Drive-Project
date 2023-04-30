from abc import ABC, abstractmethod
from constatns import response_type

class IGmail(ABC):

    @abstractmethod
    def Create_Service(self): 
        pass

    @abstractmethod
    def get_list_of_driveUrl_and_emails(self,service): 
        pass

    @abstractmethod
    def send_reply(self,service, message_id, to_email, response:response_type):
        pass

   