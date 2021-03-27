from abcs import Message
from utilities.chatid import Chatid

class ChatMessage: 
 
    @classmethod 
    def from_string(cls, message : str): 
        """Create a ChatMessage class from a string of the form: sender_private_name|receiver_chat|content""" 
 
        if message.count('|') != 2: 
            print('WARNING: the string passed had not the right number of fields (2)') 
            return None 
 
        sender_private_name, receiver_chat_id, content = message.split('|') 
        receiver_chat_id=Chatid.from_string(receiver_chat_id) 
 
        return cls(sender=sender_private_name, chat=receiver_chat_id, content=content) 
 
    def __init__(self, sender : str, chat: Chatid,  content : str): 
        self.__sender_private_name=sender 
        self.__receiver_chat_id=chat 
        self.__content = content 
 
    def get_sender(self): 
        return self.__sender_private_name 
 
    def get_chat(self): 
        return self.__receiver_chat_id 
 
    def get_content(self): 
        return self.__content 
 
    def __str__(self): 
        return f'{self.__sender_private_name}|{self.__receiver_chat_id}|{self.__content}' 


class AccessMessage:

    @classmethod
    def from_string(cls, message : str):

        if message.count('|') != 2:
            print('WARNING: the string passed had not the right number of fields (1)')
            return None

        private_name, password, email= message.split('|')

        return cls(private_name=private_name, password=password, email=email)

    def __init__(self, private_name, password, email):
        self.__private_name=private_name
        self.__password=password
        self.__email=email

    def get_private_name(self):
        return self.__private_name

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def __str__(self):
        return f'{self.__private_name}|{self.__password}|{self.__email}'
