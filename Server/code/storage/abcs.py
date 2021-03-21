import abc

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

class CredentialStorage(abc.ABC):
    @abc.abstractmethod
    def is_user_existing(self, private_name : str) -> bool:
        ...

    @abc.abstractmethod
    def set_credential(self, private_name : str, key : str, value) -> bool:
        ...

    @abc.abstractmethod
    def get_credential(self, private_name : str, key : str) -> bool:
        ...

    #no "remove_credential" perchè non ha senso

