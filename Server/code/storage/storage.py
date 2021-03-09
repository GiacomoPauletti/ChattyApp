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


class UserTextLogger(UserLogger):
    def __init__(self):
        self.__error_description=''

    def login(self, private_name : str, password : str) -> bool:
        ...
        has_logged=True
        return has_logged

    def get_error_description(self) -> str:
        return self.__error_description

class UserTextRegister(UserRegister):
    def __init__(self):
        self.__error_description=''

    def register(self, private_name : str, password : str) -> bool:
        ...
        has_registered=True
        return has_registered

    def get_error_description(self) -> str:
        return self.__error_description

class UserTextAccesserFactory(UserAccesserFactory):
    def  get_logger(self):
        return UserTextLogger()

    def get_register(self):
        return UserTextRegister
