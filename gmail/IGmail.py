from abc import ABC, abstractmethod
from files.constatns import *

class IGmail(ABC):

    @abstractmethod
    def Create_Service(self): 
        pass

    @abstractmethod
    def get_list_of_requesrIDs_and_massageIDs(self,service): 
        pass

    @abstractmethod
    def send_reply(self,service, message_id, to_email, response:response_type):
        pass

   