import abc
from message.abcs import Message

class UserLogger(abc.ABC):
    @abc.abstractmethod
    def login(self, private_name : str, password : str) -> bool:
        ...

    def get_error_description(self) -> str:
        ...

class UserRegister(abc.ABC):
    @abc.abstractmethod
    def register(self, private_name : str, password : str) -> bool:
        ...

    def get_error_description(self) -> str:
        ...

class UserAccesserFactory(abc.ABC):
    @abc.abstractmethod
    def get_logger(self):
        ...

    @abc.abstractmethod
    def get_register(self):
        ...


class TextUserLogger(UserLogger):
    def __init__(self):
        self.__error_description=''

    def login(self, private_name : str, password : str) -> bool:
        ...
        has_logged=True
        return has_logged

    def get_error_description(self) -> str:
        return self.__error_description

class TextUserRegister(UserRegister):
    def __init__(self):
        self.__error_description=''

    def register(self, private_name : str, password : str) -> bool:
        ...
        has_registered=True
        return has_registered

    def get_error_description(self) -> str:
        return self.__error_description

class TextUserAccesserFactory(UserAccesserFactory):
    def  get_logger(self):
        return UserTextLogger()

    def get_register(self):
        return UserTextRegister


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
