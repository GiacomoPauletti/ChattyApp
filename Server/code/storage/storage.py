import abc
from message.abcs import Message



class DatabaseConstructor(abc.ABC):
    @abc.abstractmethod
    def construct(self):
        ...

class TextDatabaseConstructor(DatabaseConstructor):
    def construct(self):
        pass

class UserStorage(abc.ABC):
    @abc.abstractmethod
    def get_user_info(self, private_name : str) -> dict:
        ...

    @abc.abstractmethod
    def get_user_chats(self, private_name : str) -> dict:
        ...

    @abc.abstractmethod
    def get_user_unread_messages(self, private_name : str, chat=None) -> Message:
        #si potrebbe fare che ritorna un iterator o che funziona da iterator
        #così da dare un messaggio alla volta
        ...

class TextUserStorage(abc.ABC):
    def __init__(self):
        pass

    def get_user_info(self, private_name : str) -> dict:
        pass

    def get_user_chats(self, private_name : str) -> dict:
        pass

    def get_user_unread_messages(self, private_name : str, chat=None) -> Message:
        pass
