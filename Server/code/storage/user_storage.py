import abc
from message.abcs import Message
import message.message as msg
from utilities.chatid import Chatid
from user.abcs import User
import os

class TextUserStorageFactory:
    def __init__(self, default_path='./database/users'):
        self.__notification_storage=TextNotificationStorage(msg.NotificationMessage, default_path=default_path)
        self.__unread_chat_storage=TextUnreadChatStorage(default_path=default_path)
        self.__credential_storage=TextCredentialStorage(default_path=default_path)

        self.__default_path=default_path

    def get_user_creator(self):
        return TextUserCreator(self.__notification_storage, self.__unread_chat_storage, self.__credential_storage, self.__default_path)

    def get_notification_storage(self):
        return self.__notification_storage

    def get_unread_chat_storage(self):
        return self.__unread_chat_storage

    def get_credential_storage(self):
        return self.__credential_storage

class UserCreator:
    @abc.abstractmethod
    def new_user(self, private_name : str, credentials : dict):
        ...

    @abc.abstractmethod
    def is_user_existing(self, private_name : str):
        ...

class TextUserCreator(UserCreator):
    def __init__(self, notification_storage, unread_chat_storage, credential_storage, default_path='./database/users'):
        self.__notification_storage=notification_storage
        self.__unread_chat_storage=unread_chat_storage
        self.__credential_storage=credential_storage

        self.__default_path=default_path.rstrip('/')

    def new_user(self, private_name : str, credentials : dict):

        if self.is_user_existing(private_name):
            return None

        print(f'[UserStorage] the user {private_name} has been created')

        new_user_path=self.__default_path + f'/{private_name}'
        os.mkdir(new_user_path)

        self.__notification_storage._new_user(private_name)
        self.__unread_chat_storage._new_user(private_name)
        self.__credential_storage._new_user(private_name, credentials)

        return True
        
    def is_user_existing(self, private_name : str):
        all_users=os.walk(self.__default_path).__next__()[1]

        is_user_existing=private_name in all_users

        if not is_user_existing:
            print(f'[GeneralUserStorage] the user {private_name} is not existing')
            return False

        return True

class CredentialStorage(abc.ABC):
    @abc.abstractmethod
    def _new_user(self, private_name : str, credentials : dict):
        ...
    
    @abc.abstractmethod
    def set(self, private_name : str, key : str, value) -> bool:
        ...
        
    @abc.abstractmethod
    def get(self, private_name : str, key : str) -> bool:
        ...

    
class TextCredentialStorage(CredentialStorage):
    def __init__(self, credential_types: dict = ('private_name', 'email', 'password'), default_path='./database/users'):
        self.__credential_types=credential_types
        self.__default_path=default_path.rstrip('/')

    def _new_user(self, private_name : str, credentials : dict):
        credentials_path=self.__default_path + f'/{private_name}/credentials.txt'
        with open(credentials_path, 'w') as f:

            for credential_type in self.__credential_types:
                credential_value=credentials[credential_type]
                f.write(f'{credential_type}:{credential_value}\n')

    def is_user_existing(self, private_name : str):
        all_users=os.walk(self.__default_path).__next__()[1]

        is_user_existing=private_name in all_users

        if not is_user_existing:
            return False

        return True

    def set(self, private_name : str, key : str, value) -> bool:

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
            for credential_type, credential_value in credentials.items():
                f.write(f'{credential_type}:{credential_value}\n')

        return True            

    def get(self, private_name : str, key) -> bool:

        if not self.is_user_existing(private_name):
            return False

        for credential_type, credential_value in self.__get_all_credentials(private_name):
            if credential_type == key:
                return credential_value

        print(f'[CredentialStorage] the credential type {key} is not valid')
        return None

    def __get_all_credentials(self, private_name : str):
        credentials_path=self.__default_path + f'/{private_name}/credentials.txt'

        with open(credentials_path, 'r') as f:
            for index, line in enumerate(f):
                line=line.rstrip('\n')
                credential_type, credential_value = line.split(':')
                yield (credential_type, credential_value)

class NotificationStorage(abc.ABC):
    @abc.abstractmethod
    def _new_user(self, private_name : str):
        ...

    @abc.abstractmethod
    def add(self, private_name : str, notification):
        ...

    @abc.abstractmethod
    def get(self, private_name : str, end=1):
        ...

    @abc.abstractmethod
    def remove(self, private_name : str, end=1):
        ...

class TextNotificationStorage(NotificationStorage):
    def __init__(self, notif_message_class, default_path='./database/users'):
        self.__NotificationMessage=notif_message_class
        self.__default_path=default_path.rstrip('/')

    def _new_user(self, private_name : str):
        open(f'{self.__default_path}/{private_name}/notifications.txt', 'w')
        
    def is_user_existing(self, private_name : str):
        all_users=os.walk(self.__default_path).__next__()[1]

        is_user_existing=private_name in all_users

        if not is_user_existing:
            return False

        return True
        
    def add(self, private_name : str, notification):

        if not self.is_user_existing(private_name):
            return False

        notifications_path=self.__default_path + f'/{private_name}/notifications.txt'
        with open(notifications_path, 'a') as f:
            f.write(f'{str(notification)}\n')

    def get(self, private_name : str, end=None) -> str:
        
        if not self.is_user_existing(private_name):
            return False
        
        notifications_path=self.__default_path + f'/{private_name}/notifications.txt'

        with open(notifications_path, 'r') as f:
            for index, notif in enumerate(f):
                if end==None or index < end:
                    notif=notif.rstrip('\n')
                    
                    final_notif=self.__NotificationMessage.from_string(notif)
                    yield final_notif

    def remove(self, private_name : str, end=1):
        
        if not self.is_user_existing(private_name):
            return False

        notifications_path=self.__default_path + f'/{private_name}/notifications.txt'
        with open(notifications_path, 'r') as f:
            notifications=f.readlines()

        with open(notifications_path, 'w') as f:
            for index,notif in enumerate(notifications):
                if index >= end:
                    f.write(notif)


class UnreadChatStorage(abc.ABC):
    @abc.abstractmethod
    def _new_user(self, private_name : str):
        ...

    @abc.abstractmethod
    def add(self, private_name : str, chat : Chatid):
        ...

    @abc.abstractmethod
    def get(self, private_name : str, end=1):
        ...

    @abc.abstractmethod
    def remove(self, private_name : str, end=1):
        ...

class TextUnreadChatStorage(UnreadChatStorage):
    def __init__(self, default_path='./database/users'):
        self.__default_path=default_path.rstrip('/')

    def _new_user(self, private_name : str):
        new_unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        open(new_unread_chat_path, 'w')

    def is_user_existing(self, private_name : str):
        all_users=os.walk(self.__default_path).__next__()[1]

        is_user_existing=private_name in all_users

        if not is_user_existing:
            return False

        return True

    def add(self, private_name : str, chat : Chatid):

        if not self.is_user_existing(private_name):
            return False

        unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        with open(unread_chat_path, 'a') as f:
            f.write(f'{str(chat)}\n')

    def get(self, private_name : str, end=None):

        if not self.is_user_existing(private_name):
            return False

        unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        with open(unread_chat_path, 'r') as f:
            for index, chat in enumerate(f):
                if end==None or index < end:
                    chat=chat.rstrip('\n')
                    
                    final_chat=Chatid.from_string(chat)
                    yield final_chat

    def remove(self, private_name : str, end=1):

        if not self.is_user_existing(private_name):
            return False

        unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        with open(unread_chat_path, 'r') as f:
            unread_chats=f.readlines()

        with open(unread_chat_path, 'w') as f:
            for index,chat in enumerate(unread_chats):
                if index >= end:
                    f.write(chat)

