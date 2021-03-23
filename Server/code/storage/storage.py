import abc
from message.abcs import Message
from utilities.chatid import Chatid
from user.abcs import User
import os

class GeneralUserStorage(abc.ABC):
    @abc.abstractmethod
    def new_user(self, private_name : str, credentials : dict):
        ...

    @abc.abstractmethod
    def is_user_existing(self, private_name : str):
        ...

class TextGeneralUserStorage(GeneralUserStorage):
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

        self.__notification_storage.new_user(private_name)
        self.__unread_chat_storage.new_user(private_name)
        self.__credential_storage.new_user(private_name, credentials)
        
    def is_user_existing(self, private_name : str):
        all_users=os.walk(self.__default_path).__next__()[1]

        is_user_existing=private_name in all_users

        if not is_user_existing:
            print(f'[GeneralUserStorage] the user {private_name} is not existing')
            return False

        return True

class CredentialStorage(abc.ABC):
    @abc.abstractmethod
    def new_user(self, private_name : str, credentials : dict):
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

    def new_user(self, private_name : str, credentials : dict):
        credentials_path=self.__default_path + f'/{private_name}/credentials.txt'
        with open(credentials_path, 'w') as f:

            for credential_type in self.__credential_types:
                credential_value=credentials[credential_type]
                f.write(f'{credential_type}:{credential_value}\n')


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
    def new_user(self, private_name : str):
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

    def new_user(self, private_name : str):
        open(f'{self.__default_path}/{private_name}/notifications.txt', 'w')
        
    def add(self, private_name : str, notification):


        notifications_path=self.__default_path + f'/{private_name}/notifications.txt'
        with open(notifications_path, 'a') as f:
            f.write(f'{str(notification)}\n')

    def get(self, private_name : str, end=None) -> str:
        
        notifications_path=self.__default_path + f'/{private_name}/notifications.txt'

        with open(notifications_path, 'r') as f:
            for index, notif in enumerate(f):
                if end==None or index < end:
                    notif=notif.rstrip('\n')
                    
                    final_notif=self.__NotificationMessage.from_string(notif)
                    yield final_notif

    def remove(self, private_name : str, end=1):
        
        notifications_path=self.__default_path + f'/{private_name}/notifications.txt'
        with open(notifications_path, 'r') as f:
            notifications=f.readlines()

        with open(notifications_path, 'w') as f:
            for index,notif in enumerate(notifications):
                if index >= end:
                    f.write(notif)


class UnreadChatStorage(abc.ABC):
    @abc.abstractmethod
    def new_user(self, private_name : str):
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

    def new_user(self, private_name : str):
        new_unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        open(new_unread_chat_path, 'w')

    def add(self, private_name : str, chat : Chatid):
        unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        with open(unread_chat_path, 'a') as f:
            f.write(f'{str(chat)}\n')

    def get(self, private_name : str, end=None):

        unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        with open(unread_chat_path, 'r') as f:
            for index, chat in enumerate(f):
                if end==None or index < end:
                    chat=chat.rstrip('\n')
                    
                    final_chat=Chatid.from_string(chat)
                    yield final_chat

    def remove(self, private_name : str, end=1):

        unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        with open(unread_chat_path, 'r') as f:
            unread_chats=f.readlines()

        with open(unread_chat_path, 'w') as f:
            for index,chat in enumerate(unread_chats):
                if index >= end:
                    f.write(chat)


class UserStorage:
    def __init__(self, notification_storage, unread_chat_storage, general_user_storage, default_path='./database/users'):
        self.__notification_storage=notification_storage
        self.__unread_chat_storage=unread_chat_storage
        self.__general_user_storage=general_user_storage

        self.__default_path=default_path.rstrip('/')

    def new_user(self, private_name : str, credentials):
        self.__general_user_storage.new_user(private_name, credentials) 
        
    def is_user_existing(self, private_name : str):
        return self.__general_user_storage.is_user_existing(private_name)
        
    def add_unread_chat(self, private_name : str, chat : Chatid):
        if not self.is_user_existing(private_name):
            return None

        self.__unread_chat_storage.add(private_name, chat)

    def get_unread_chats(self, private_name : str, end=None):
        if not self.is_user_existing(private_name):
            return None

        yield from self.__unread_chat_storage.get(private_name, end)

    def remove_unread_chats(self, private_name : str, end=1):
        if not self.is_user_existing(private_name):
            return None

        self.__unread_chat_storage.remove(private_name, end)

    def add_notification(self, private_name : str, notification):
        if not self.is_user_existing(private_name):
            return None

        self.__notification_storage.add(private_name, notification)

    def get_notifications(self, private_name : str, end=None):
        if not self.is_user_existing(private_name):
            return None

        yield from self.__notification_storage.get(private_name, end)

    def remove_notifications(self, private_name, end=1):
        if not self.is_user_existing(private_name):
            return None

        self.__notification_storage.remove(private_name, end)



class ChatCreator:
    def __init__(self, message_storage : MessageStorage, user_chat_storage : UserChatStorage, default_path='./database/chats'):
        self.__message_storage=message_storage
        self.__user_chat_storage=user_chat_storage
        
        self.__default_path=default_path

    def new_chat(self, chatid : Chatid):
        if self.is_chat_existing(chatid):
            return None

        print(f'[ChatStorage] the chat {chatid} has been created')

        new_chat_path=self.__default_path+f'/{str(chatid)}'
        os.mkdir(new_chat_path)

        self.__message_storage._new_chat(chatid)
        self.__user_chat_storage._new_chat(chatid)
        
    def is_chat_existing(self, chatid : Chatid) -> bool:
        all_chats=os.walk(self.__default_path).__next__()[1]  

        is_chat_existing=str(chatid) in all_chats 
        if not is_chat_existing: 
            print(f'[ChatStorage] the chat {str(chatid)} is not existing') 
            return False 

        return True 


def _get_num_of_lines(path):
    with open(path, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i+1

class UserChatStorage(abc.ABC):

    @abc.abstractmethod
    def _new_chat(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def add_user(self, chatid : Chatid, private_name : str):
        ...

    @abc.abstractmethod
    def __get_indexes(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def get_user_index(self, chatid : Chatid, private_name : str):
        ...

    @abc.abstractmethod
    def increment_user_index(self, chatid : Chatid, private_name : str, incrementor=1) -> None:
        ...

    @abc.abstractmethod 
    def get_maximum_index(self, chatid : Chatid) -> int:
        ...

class TextUserChatStorage(UserChatStorage):
    def __init__(self, default_path='./database/chats'):
        self.__default_path=default_path

    def _new_chat(self, chatid : Chatid):
        
        if self.is_chat_existing(chatid):
            return None

        new_chat_path=self.__default_path+f'/{str(chatid)}'
        os.mkdir(new_chat_path)

        open(new_chat_path + f'/users.txt', 'w')

    def is_chat_existing(self, chatid : Chatid) -> bool:
        all_chats=os.walk(self.__default_path).__next__()[1]  

        is_chat_existing=str(chatid) in all_chats 
        if not is_chat_existing: 
            print(f'[ChatStorage] the chat {str(chatid)} is not existing') 
            return False 

        return True 

    def add_user(self, chatid : Chatid, private_name : str):

        if not self.is_chat_existing(chatid):
            return None

        if self.get_user_index('the_chat', private_name):
            return False

        user_chat_path=self.__default_path + f'/{str(chatid)}/users.txt'
        
        for user, index in self.get_indexes(chatid): 
            if user == private_name:
                print(f'[ChatStorage] the user {private_name} has already been added to {str(chatid)}')
                return None

        open(user_chat_path, 'a').write(f'{private_name}:0\n')

        return True

    def __get_indexes(self, chatid : Chatid):
        """
        TextUserChatStorage.get_indexes(self, chatid)

        It is an iterator which yields the user and the respective index of the passed chat, if it exists
        """

        if not self.is_chat_existing(chatid):
            return None

        user_chat_path=self.__default_path + f'/{str(chatid)}/users.txt'

        lines=open(user_chat_path, 'r').readlines()
        if len(lines)==0:
            return None

        users_indexes={user:int(index) for user,index in [(line.split(':')) for line in lines]}
        
        for user, index in users_indexes.items():
            yield (user, index)
    
    def get_user_index(self, chatid : Chatid, private_name : str):
        """
        TextUserChatStorage.get_user_index(eslf, chatid, private_name)

        It returns the index of the last message read/received by the user
        """

        if not self.is_chat_existing(chatid):
            return None

        for user, index in self.get_indexes(chatid):
            if user==private_name:
                return index
        else:
            return None

    def increment_user_index(self, chatid : Chatid, private_name : str, incrementor=1) -> None:
        """
        TextUserChatStorage.increment_user_index(self, chatid, private_name)

        It increments by 'incrementor' the index of the passed user
        """ 

        user_indexes={user:index for user, index in self.get_indexes(chatid)}
        if not user_indexes:
            return None
        
        if not private_name in user_indexes.keys():
            return None

        user_indexes[private_name] += incrementor

        user_chat_path=self.__default_path + f'/{str(chatid)}/users.txt'
        with open(user_chat_path, 'w') as f:
            for user, index in user_indexes.items():
                f.write(f'{user}:{index}\n')

    def __get_maximum_index(self, chatid : Chatid) -> int:
        """
        TextUserChatStorage.get_maximum_index(self, chatid)

        It returns the index of the most recent message of the chat, which is the maiximum index.
        The passed chat must exist already
        """

        if not self.is_chat_existing(chatid):
            return None

        messages_chat_path=self.__default_path+f'/{str(chatid)}/messages.txt'        
        return _get_num_of_lines(messages_chat_path)

class MessageStorage(abc.ABC):
    @abc.abstractmethod
    def _new_chat(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def add_message(self, chatid : Chatid, message : Message):
        ...

    @abc.abstractmethod
    def get_messages(self, chatid : Chatid, start : int, end : int) -> Message:
        ...

class TextMessageStorage(MessageStorage):
    def __init__(self, chat_message_class, default_path='./database/chats'):
        self.__ChatMessage=chat_message_class
        
        self.__default_path=default_path

    def _new_chat(self, chatid: Chatid):
        new_chat_path=self.__default_path+f'/{str(chatid)}'
        os.mkdir(new_chat_path)

        open(new_chat_path + f'/messages.txt', 'w')

    def is_chat_existing(self, chatid : Chatid) -> bool:
        all_chats=os.walk(self.__default_path).__next__()[1]  

        is_chat_existing=str(chatid) in all_chats 
        if not is_chat_existing: 
            print(f'[ChatStorage] the chat {str(chatid)} is not existing') 
            return False 

        return True 

    def add_message(self, chatid : Chatid, message : Message):

        if not self.is_chat_existing(chatid):
            return None

        messages_chat_path=self.__default_path + f'/{chatid}/messages.txt'
        with open(messages_chat_path, 'a') as msg_file:
            msg_file.write(f'{str(message)}\n')

    def get_messages(self, chatid : Chatid, start : int, end : int) -> Message:
        if not self.is_chat_existing(chatid):
            return None
        
        if end < start or start < 0:
            return None
        
        messages_chat_path=self.__default_path+f'/{str(chatid)}/messages.txt'
        with open(messages_chat_path, 'r') as f:
            for index, message in enumerate(f):
                if start <= index < end:
                    message.rstrip('\n')
                    final_message=self.__ChatMessage.from_string(message)
                    yield final_message
"""
class ChatStorage(abc.ABC):
    @abc.abstractmethod
    def new_chat(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def is_chat_existing(self, chatid : Chatid) -> bool:
        ...

    @abc.abstractmethod
    def add_user(self, chatid : Chatid, private_name : str):
        ...

    @abc.abstractmethod
    def get_indexes(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def get_user_index(self, chatid : Chatid, private_name : str):
        ...

    @abc.abstractmethod
    def increment_user_index(self, chatid : Chatid, private_name : str, incrementor=1) -> None:
        ...

    @abc.abstractmethod 
    def get_maximum_index(self, chatid : Chatid) -> int:
        ...

    @abc.abstractmethod
    def add_message(self, chatid : Chatid, message : Message):
        ...

    @abc.abstractmethod
    def get_messages(self, chatid : Chatid, start : int, end : int) -> Message:
        ...

def _get_num_of_lines(path):
    with open(path, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i+1
    
class TextChatStorage(ChatStorage):
    def __init__(self, chat_message_class, default_path='./database/chats'):
        self.__default_path=default_path.rstrip('/')
        self.__ChatMessage=chat_message_class

    def new_chat(self, chatid : Chatid):
        TextChatStorage.new_chat(self, chatid)

        It creates the database for a new chat, if it hasn't been created yet

        if self.is_chat_existing(chatid):
            return None

        print(f'[ChatStorage] the chat {chatid} has been created')

        new_chat_path=self.__default_path+f'/{str(chatid)}'
        os.mkdir(new_chat_path)

        open(new_chat_path + f'/messages.txt', 'w')
        open(new_chat_path + f'/users.txt', 'w')

    def is_chat_existing(self, chatid : Chatid) -> bool:
        all_chats=os.walk(self.__default_path).__next__()[1]  

        is_chat_existing=str(chatid) in all_chats 
        if not is_chat_existing: 
            print(f'[ChatStorage] the chat {str(chatid)} is not existing') 
            return False 

        return True 

    def add_user(self, chatid : Chatid, private_name : str):
        TextChatStorage.add_user(self, chatid, private_name)

        It adds the user whose private_name is passed to the passed chat database, if both existing
    
        if not self.is_chat_existing(chatid):
            return None

        user_chat_path=self.__default_path + f'/{str(chatid)}/users.txt'
        
        for user, index in self.get_indexes(chatid): 
            if user == private_name:
                print(f'[ChatStorage] the user {private_name} has already been added to {str(chatid)}')
                return None

        open(user_chat_path, 'a').write(f'{private_name}:0\n')

    def get_indexes(self, chatid : Chatid):
        TextChatStorage.get_indexes(self, chatid)

        It is an iterator which yields the user and the respective index of the passed chat, if it exists

        if not self.is_chat_existing(chatid):
            return None

        user_chat_path=self.__default_path + f'/{str(chatid)}/users.txt'

        lines=open(user_chat_path, 'r').readlines()
        if len(lines)==0:
            return None

        users_indexes={user:int(index) for user,index in [(line.split(':')) for line in lines]}
        
        for user, index in users_indexes.items():
            yield (user, index)

    def get_user_index(self, chatid : Chatid, private_name : str):
        TextChatStorage.get_user_index(eslf, chatid, private_name)

        It returns the index of the last message read/received by the user

        if not self.is_chat_existing(chatid):
            return None

        for user, index in self.get_indexes(chatid):
            if user==private_name:
                return index
        else:
            return None


    def increment_user_index(self, chatid : Chatid, private_name : str, incrementor=1) -> None:
        TextChatStorage.increment_user_index(self, chatid, private_name)

        It increments by 'incrementor' the index of the passed user

        user_indexes={user:index for user, index in self.get_indexes(chatid)}
        if not user_indexes:
            return None
        
        if not private_name in user_indexes.keys():
            return None

        user_indexes[private_name] += incrementor

        user_chat_path=self.__default_path + f'/{str(chatid)}/users.txt'
        with open(user_chat_path, 'w') as f:
            for user, index in user_indexes.items():
                f.write(f'{user}:{index}\n')
        


    def get_maximum_index(self, chatid : Chatid) -> int:
        TextChatStorage.get_maximum_index(self, chatid)

        It returns the index of the most recent message of the chat, which is the maiximum index.
        The passed chat must exist already

        if not self.is_chat_existing(chatid):
            return None

        messages_chat_path=self.__default_path+f'/{str(chatid)}/messages.txt'        
        return _get_num_of_lines(messages_chat_path)

    def add_message(self, chatid : Chatid, message : Message):

        if not self.is_chat_existing(chatid):
            return None

        messages_chat_path=self.__default_path + f'/{chatid}/messages.txt'
        with open(messages_chat_path, 'a') as msg_file:
            msg_file.write(f'{str(message)}\n')

    def get_messages(self, chatid : Chatid, start : int, end : int) -> Message:
        TextChatStorage.get_messages(self, chatid, start, end) 

        It is an iterator which yields the messages between the start and end of the passed chat (if it exists)
        
        Both messages at index 'start' and 'end' are yielded

        if not self.is_chat_existing(chatid):
            return None
        
        if end < start or start < 0:
            return None
        
        end = end if end < self.get_maximum_index(chatid) else self.get_maximum_index(chatid)

        messages_chat_path=self.__default_path+f'/{str(chatid)}/messages.txt'
        with open(messages_chat_path, 'r') as f:
            for index, message in enumerate(f):
                if start <= index <= end:
                    message.rstrip('\n')
                    final_message=self.__ChatMessage.from_string(message)
                    yield final_message


class UserStorage(abc.ABC):
    @abc.abstractmethod
    def new_user(self, private_name : str):
        ...

    @abc.abstractmethod
    def is_user_existing(self, private_name : str):
        ...

    @abc.abstractmethod
    def add_unread_chat(self, private_name : str, chat : Chatid):
        ...

    @abc.abstractmethod
    def get_unread_chats(self, private_name : str, end=None):
        ...

    @abc.abstractmethod
    def remove_unread_chats(self, private_name : str, end=1):
        ...

    @abc.abstractmethod
    def get_notifications(self, private_name : str, end=None):
        ...

    @abc.abstractmethod
    def remove_notifications(self, private_name, end=1):
        ...
"""

"""
class TextUserStorage(UserStorage):
    def __init__(self, notif_message_class, default_path='./database/users'):
        self.__default_path=default_path.rstrip('/')
        self.__NotificationMessage=notif_message_class

    def new_user(self, private_name : str):

        if self.is_user_existing(private_name):
            return None

        print(f'[UserStorage] the user {private_name} has been created')

        new_user_path=self.__default_path + f'/{private_name}'
        os.mkdir(new_user_path)

        open(new_user_path + f'/credentials.txt', 'w')
        open(new_user_path + f'/unread_chats.txt', 'w') #OPPURE LAST_CHATS.TXT
        open(new_user_path + f'/notifications.txt', 'w')

    def is_user_existing(self, private_name : str):
        all_users=os.walk(self.__default_path).__next__()[1]

        is_user_existing=private_name in all_users

        if not is_user_existing:
            print(f'[UserStorage] the user {private_name} is not existing')
            return False

        return True

    def add_unread_chat(self, private_name : str, chat : Chatid):
        
        if not self.is_user_existing(private_name):
            return None

        unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        with open(unread_chat_path, 'a') as f:
            f.write(f'{str(chat)}\n')

    def get_unread_chats(self, private_name : str, end=None):
        
        if not self.is_user_existing(private_name):
            return None

        unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        with open(unread_chat_path, 'r') as f:
            for index, chat in enumerate(f):
                if end==None or index < end:
                    chat=chat.rstrip('\n')
                    
                    final_chat=Chatid.from_string(chat)
                    yield final_chat

    def remove_unread_chats(self, private_name : str, end=1):
        
        if not self.is_user_existing(private_name):
            return None

        unread_chat_path=self.__default_path + f'/{private_name}/unread_chats.txt'
        with open(unread_chat_path, 'r') as f:
            unread_chats=f.readlines()

        with open(unread_chat_path, 'w') as f:
            for index,chat in enumerate(unread_chats):
                if index >= end:
                    f.write(chat)
"""
