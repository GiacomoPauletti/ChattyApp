import abc
from message.abcs import Message
from utilities.chatid import Chatid
from user.abcs import User
import os

            
class UserStorage(abc.ABC):
    @abc.abstractmethod
    def new_user(self, private_name : str):
        ...

    @abc.abstractmethod
    def get_chats(self, private_name : str) -> dict:
        ...

    @abc.abstractmethod
    def get_notifications(self, private_name : str) -> str:
        ...

    @abc.abstractmethod
    def get_unread_messages(self, private_name : str, chat=None) -> Message:
        #si potrebbe fare che ritorna un iterator o che funziona da iterator
        #così da dare un messaggio alla volta
        ...

class TextUserStorage(abc.ABC):
    def __init__(self):
        pass

    def new_user(self, private_name : str):
        pass

    def get_chats(self, private_name : str) -> dict:
        pass

    def get_notifications(self, private_name : str) -> str:
        ...

    def get_unread_messages(self, private_name : str, chat: Chatid) -> Message:
        pass


class ChatStorage(abc.ABC):
    @abc.abstractmethod
    def new_chat(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def get_info(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def get_users(self, chatid : Chatid):
        ...

    @abc.abstractmethod 
    def get_maximum_index(self, chatid : Chatid) -> int:
        ...

    @abc.abstractmethod
    def get_message_at_index(self, chatid : Chatid, index : int) -> Message:
        ...

    @abc.abstractmethod
    def get_user_index(self, chatid : Chatid, user : User) -> int:
        ...

    @abc.abstractmethod
    def increment_user_index(self, chatid : Chatid, user : User) -> None:
        ...

    
