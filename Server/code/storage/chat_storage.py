import abc
from message.abcs import Message
import message.message as msg
from utilities.chatid import Chatid
from user.abcs import User
import os


class TextChatStorageFactory:
    def __init__(self, default_path='./database/chats'):
        self.__user_chat_storage=TextUserChatStorage(default_path=default_path)
        self.__message_storage=TextMessageStorage(chat_message_class=msg.ChatMessage, default_path=default_path)

        self.__default_path=default_path

    def get_chat_storage_creator(self):
        return TextChatStorageCreator(self.__message_storage, self.__user_chat_storage, self.__default_path)

    def get_user_chat_storage(self):
        return self.__notification_storage

    def get_message_storage(self):
        return self.__message_storage


class ChatStorageCreator(abc.ABC):
    @abc.abstractmethod
    def new_chat(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def is_chat_existing(self, chatid : Chatid):
        ...

class TextChatStorageCreator(ChatStorageCreator):
    def __init__(self, message_storage, user_chat_storage, default_path='./database/chats'):
        self.__message_storage=message_storage
        self.__user_chat_storage=user_chat_storage
        
        self.__default_path=default_path

    def new_chat(self, chatid : Chatid):
        if self.is_chat_existing(chatid):
            return False

        print(f'[ChatStorage] the chat {chatid} has been created')

        new_chat_path=self.__default_path+f'/{str(chatid)}'
        os.mkdir(new_chat_path)

        self.__message_storage._new_chat(chatid)
        self.__user_chat_storage._new_chat(chatid)

        return True
        
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
    def get_users(self, chatid : Chatid):
        ...
        
    @abc.abstractmethod
    def remove_user(self, chatid : Chatid, private_name : str):
        ...

    def __get_indexes(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def get_user_index(self, chatid : Chatid, private_name : str):
        ...

    @abc.abstractmethod
    def increment_user_index(self, chatid : Chatid, private_name : str, incrementor=1) -> None:
        ...

    def get_maximum_index(self, chatid : Chatid) -> int:
        ...

class TextUserChatStorage(UserChatStorage):
    def __init__(self, default_path='./database/chats'):
        self.__default_path=default_path

    def _new_chat(self, chatid : Chatid):
        
        new_users_path=self.__default_path+f'/{str(chatid)}/users.txt'
        open(new_users_path, 'w')

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

        if self.get_user_index(chatid, private_name):
            return False

        user_chat_path=self.__default_path + f'/{str(chatid)}/users.txt'
        
        for user, index in self.__get_indexes(chatid): 
            if user == private_name:
                print(f'[ChatStorage] the user {private_name} has already been added to {str(chatid)}')
                return None

        open(user_chat_path, 'a').write(f'{private_name}:0\n')

        return True

    def get_users(self, chatid : Chatid):
        for user, index in self.__get_indexes(chatid):
            yield user

    def remove_user(self, chatid : Chatid, private_name : str):

        user_chat_path=self.__default_path + f'/{str(chatid)}/users.txt'

        indexes={user:index for user, index in self.__get_indexes(chatid)}

        with open(user_chat_path, 'w') as f:
            for user, index in indexes.items():
                if not user == private_name:
                    f.write(f'{user}:{index}\n')

        return True
                    

    def __get_indexes(self, chatid : Chatid):
        """
        TextUserChatStorage.__get_indexes(self, chatid)

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

        for user, index in self.__get_indexes(chatid):
            if user==private_name:
                return index
        else:
            return None

    def increment_user_index(self, chatid : Chatid, private_name : str, incrementor=1) -> None:
        """
        TextUserChatStorage.increment_user_index(self, chatid, private_name)

        It increments by 'incrementor' the index of the passed user
        """ 

        user_indexes={user:index for user, index in self.__get_indexes(chatid)}
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

        new_message_path=self.__default_path+f'/{str(chatid)}/messages.txt'
        open(new_message_path, 'w')

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
