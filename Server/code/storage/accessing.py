import abc
from message.abcs import Message

def CredentialStorage(abc.ABC):
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

def TextCredentialStorage(CredentialStorage):
    def __init__(self, credential_types: dict = ('private_name', 'email', 'password'), default_path='./database/users'):
        self.__credential_types=credential_types
        self.__default_path=default_path

    def new_user(self, private_name : str, credentials : dict):
        credentials_path=self.__default_path + f'/{private_name}/credentials.txt'
        with open(credentials_path, 'w') as f:

            for credential_type in self.__credential_types:
                credential_value=credentials[credential_type]
                f.write(f'{credential_type}:{credential_value}\n')

    def is_user_existing(self, private_name : str):
        all_users=os.walk(self.__default_path).__next__()[1]

        is_user_existing=private_name in all_users

        if not is_user_existing:
            print(f'[UserStorage] the user {private_name} is not existing')
            return False

        return True

    def set_credential(self, private_name : str, key : str, value) -> bool:

        if not self.is_user_existing(private_name):
            return False

        if not key in self.__credential_types:
            print(f'[CredentialUserStorage] credential type {key} not existing')
            return False

        credentials={}
        for credential_type, credential_value in self.__get_all_credentials(private_name):
            if credential_type == key:
                credentials[credential_type]=value
            else:
                credentials[credential_type]=credential_value

        credentials_path=self.__default_path + f'/{private_name}/credentials.txt'
        with open(credentials_path, 'w') as f:
            for credential_type, credential_value in credentials:
                f.write(f'{credential_type}:{credential_value}\n')

        return True


    def get_credential(self, private_name : str, key) -> bool:

        if not self.is_user_existing(private_name):
            return False

        for credential_type, credential_value in self.__get_all_credentials(private_name):
            if credential_type == key:
                return credential_value
        
        return None

    def __get_all_credentials(self, private_name : str):
        credentials_path=self.__default_path + f'/{private_name}/credentials.txt'

        with open(credentials_path, 'r') as f:
            for index, line in enumerate(f):
                line=line.rstrip('\n')
                credential_type, credential_value = line.split(':')
                yield (credential_type, credential_value)

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

