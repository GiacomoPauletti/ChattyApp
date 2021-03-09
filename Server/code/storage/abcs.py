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