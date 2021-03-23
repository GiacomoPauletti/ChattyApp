import abc
from message.abcs import Message
import os
import storage.user_storage as ust
import errors.errors as err


class TextUserAccesserFactory:
    def __init__(self, default_path='./database/users'):
        self.__tusf=ust.TextUserStorageFactory(default_path)
        
    def get_logger(self):
        return UserLogger(self.__tusf.get_credential_storage())

    def get_register(self):
        return UserTextRegister(self.__tusf.get_user_creator())

class UserLogger:
    def __init__(self, credential_storage):
        self.__credential_storage = credential_storage
        self.__error=None
    
    def login(self, private_name : str, password : str) -> bool:
        user_password=self.__credential_storage.get(private_name, 'password')

        if user_password==password:
            return True

        self.__error=err.AccessError('password')
        return False

    def get_error_description(self) -> str:
        return self.__error

class UserRegister:
    def __init__(self, user_creator):
        self.__user_creator=user_creator
        self.__error=None

    def register(self, private_name : str, password : str, email : str) -> bool:
        if self.__user_creator.is_user_existing(private_name):
            self.__error=err.AccessError(field='private_name', description='private name already existing')
            return False
        
        credentials={'private_name':private_name, 'email':email, 'password':password}
        if not self.__user_creator.new_user(private_name, credentials):
            self.__error=err.AccessError(field='unknown', description='unable to register with this credentials')
            return False

        return True
    
    def get_error_description(self):
        return self.__error

"""
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

"""
