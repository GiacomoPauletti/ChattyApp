import abc
from message.abcs import Message
from utilities.chatid import Chatid
from user.abcs import User
import os

            
class UserStorage(abc.ABC):
    @abc.abstractmethod
    def new_user(self, private_name : str):
        ...

    @abc.abstractmethod
    def get_chats(self, private_name : str) -> dict:
        ...

    @abc.abstractmethod
    def get_notifications(self, private_name : str) -> str:
        ...

    @abc.abstractmethod
    def get_unread_messages(self, private_name : str, chat=None) -> Message:
        #si potrebbe fare che ritorna un iterator o che funziona da iterator
        #così da dare un messaggio alla volta
        ...

class TextUserStorage(abc.ABC):
    def __init__(self):
        pass

    def new_user(self, private_name : str):
        pass

    def get_chats(self, private_name : str) -> dict:
        pass

    def get_notifications(self, private_name : str) -> str:
        ...

    def get_unread_messages(self, private_name : str, chat: Chatid) -> Message:
        pass


class ChatStorage(abc.ABC):
    @abc.abstractmethod
    def new_chat(self, chatid : Chatid):
        ...

    @abc.abstractmethod
    def get_users(self, chatid : Chatid):
        ...

    @abc.abstractmethod 
    def get_maximum_index(self, chatid : Chatid) -> int:
        ...

    @abc.abstractmethod
    def get_message_at_index(self, chatid : Chatid, index : int) -> Message:
        ...

    @abc.abstractmethod
    def get_user_index(self, chatid : Chatid, user : User) -> int:
        ...

    @abc.abstractmethod
    def increment_user_index(self, chatid : Chatid, user : User) -> None:
        ...

def _get_num_of_lines(path):
    with open(path, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i+1
    
class TextChatStorage(ChatStorage):
    def __init__(self, chats_db_path='./database/chats'):
        self.__path=chats_db_path.rstrip('/')

    def new_chat(self, chatid : Chatid):
        """
        TextChatStorage.new_chat(self, chatid)

        It creates the database for a new chat, if it hasn't been created yet
        """

        if not self.is_chat_existing(chatid):
            return None

        new_chat_path=self.__path+f'/{str(chatid)}'
        os.mkdir(new_chat_path)

        open(new_chat_path + f'/{messages.txt}')
        open(new_chat_path + f'/{users.txt}')

    def is_chat_existing(self, chatid : Chatid) -> bool:
        all_chats=os.walk(self.__path).__next__()[1]  

        is_chat_existing=str(chatid) in all_chats 
        if not is_chat_existing: 
            print(f'[ChatStorage] the chat {str(chatid)} is not existing') 
            return False 

        return True 

    def add_user(self, chatid : Chatid, private_name : str):
        """
        TextChatStorage.add_user(self, chatid, private_name)

        It adds the user whose private_name is passed to the passed chat database, if both existing
        """
    
        if not self.is_chat_existing(chatid):
            return None

        user_chat_path=self.__path + f'/{str(chatid)}/users.txt'
        

        if is_already_added:
            print(f'[ChatStorage] the user {private_name} has already been added to {str(chatid)}')
            return None

        open(chat_path, 'a').write(f'{private_name}:0}')

    def get_indexes(self, chatid : Chatid):
        """
        TextChatStorage.get_indexes(self, chatid)

        It is an iterator which yields the user and the respective index of the passed chat, if it exists
        """

        if not self.is_chat_existing(chatid):
            return None

        user_chat_path=self.__path + f'/{str(chatid)}/users.txt'

        lines=open(user_chat_path, 'r').readline().split('\n')
        users_indexes={user:int(index) for user,index in line.split(':') for line in lines}

        for user, index in users_indexes:
            yield (user, index)

    def get_user_index(self, chatid : Chatid, private_name : str):
        """
        TextChatStorage.get_user_index(eslf, chatid, private_name)

        It returns the index of the last message read/received by the user
        """

        if not self.is_chat_existing(chatid):
            return None

        for user, index in self.__get_indexes(chatid):
            if user==private_name:
                return private_name
        else:
            return None


    def increment_user_index(self, chatid : Chatid, private_name : str, incrementor=1) -> None:
        """
        TextChatStorage.increment_user_index(self, chatid, private_name)

        It increments by 'incrementor' the index of the passed user
        """ 

        user_indexes=self.get_indexes(chatid)
        if not info:
            return None
        
        if not private_name in user_indexes.keys():
            return None

        user_indexes[private_name] += incrementor

        user_chat_path=self.__path + f'/{str(chatid)}/users.txt'
        with open(user_chat_path, 'w') as f:
            for user, index in user_indexes:
                f.write(f'{user}:{index}')
        


    def get_maximum_index(self, chatid : Chatid) -> int:
        """
        TextChatStorage.get_maximum_index(self, chatid)

        It returns the index of the most recent message of the chat, which is the maiximum index.
        The passed chat must exist already
        """

        if not self.is_chat_existing(chatid):
            return None

        chat_path=self.__path+f'/{str(chatid)}'        
        return _get_num_of_lines(chat_path)

    def add_message(self, chatid : Chatid, message : Message):
        ...

    def get_messages(self, chatid : Chatid, start : int, end : int) -> Message:
        """
        TextChatStorage.get_messages(self, chatid, start, end) 

        It is an iterator which yields the messages between the start and end of the passed chat (if it exists)
        
        Both messages at index 'start' and 'end' are yielded
        """ 

        if not self.is_chat_existing(chatid):
            return None
        
        if end < start:
            return None
        
        end = end if end < self.get_maximum_index(chatid) else self.get_maximum_index(chatid)

        chat_path=self.__path+f'/{str(chatid)}'
        
        with open(chat_path, 'r') as f:
            for index, message in enumerate(f):
                if start < index < end:
                    yield message



