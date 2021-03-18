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
    def __init__(self, chats_db_path='./database/chats'):
        self.__path=chats_db_path.rstrip('/')

    def new_chat(self, chatid : Chatid):
        """
        TextChatStorage.new_chat(self, chatid)

        It creates the database for a new chat, if it hasn't been created yet
        """

        if self.is_chat_existing(chatid):
            return None

        print(f'[ChatStorage] the chat {chatid} has been created')

        new_chat_path=self.__path+f'/{str(chatid)}'
        os.mkdir(new_chat_path)

        open(new_chat_path + f'/messages.txt', 'w')
        open(new_chat_path + f'/users.txt', 'w')

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
        
        for user, index in self.get_indexes(chatid): 
            if user == private_name:
                print(f'[ChatStorage] the user {private_name} has already been added to {str(chatid)}')
                return None

        open(user_chat_path, 'a').write(f'{private_name}:0\n')

    def get_indexes(self, chatid : Chatid):
        """
        TextChatStorage.get_indexes(self, chatid)

        It is an iterator which yields the user and the respective index of the passed chat, if it exists
        """

        if not self.is_chat_existing(chatid):
            return None

        user_chat_path=self.__path + f'/{str(chatid)}/users.txt'

        lines=open(user_chat_path, 'r').readlines()
        if len(lines)==0:
            return None

        users_indexes={user:int(index) for user,index in [(line.split(':')) for line in lines]}
        
        for user, index in users_indexes.items():
            yield (user, index)

    def get_user_index(self, chatid : Chatid, private_name : str):
        """
        TextChatStorage.get_user_index(eslf, chatid, private_name)

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
        TextChatStorage.increment_user_index(self, chatid, private_name)

        It increments by 'incrementor' the index of the passed user
        """ 

        user_indexes={user:index for user, index in self.get_indexes(chatid)}
        if not user_indexes:
            return None
        
        if not private_name in user_indexes.keys():
            return None

        user_indexes[private_name] += incrementor

        user_chat_path=self.__path + f'/{str(chatid)}/users.txt'
        with open(user_chat_path, 'w') as f:
            for user, index in user_indexes.items():
                f.write(f'{user}:{index}\n')
        


    def get_maximum_index(self, chatid : Chatid) -> int:
        """
        TextChatStorage.get_maximum_index(self, chatid)

        It returns the index of the most recent message of the chat, which is the maiximum index.
        The passed chat must exist already
        """

        if not self.is_chat_existing(chatid):
            return None

        messages_chat_path=self.__path+f'/{str(chatid)}/messages.txt'        
        return _get_num_of_lines(messages_chat_path)

    def add_message(self, chatid : Chatid, message : Message):

        if not self.is_chat_existing(chatid):
            return None

        messages_chat_path=self.__path + f'/{chatid}/messages.txt'
        with open(messages_chat_path, 'a') as msg_file:
            msg_file.write(f'{message.get_content()}\n')

    def get_messages(self, chatid : Chatid, start : int, end : int) -> Message:
        """
        TextChatStorage.get_messages(self, chatid, start, end) 

        It is an iterator which yields the messages between the start and end of the passed chat (if it exists)
        
        Both messages at index 'start' and 'end' are yielded
        """ 

        #DA SISTEMARE: bisogna salvare anche il destinatario del messaggio
        
        if not self.is_chat_existing(chatid):
            return None
        
        if end < start or start < 0:
            return None
        
        end = end if end < self.get_maximum_index(chatid) else self.get_maximum_index(chatid)

        messages_chat_path=self.__path+f'/{str(chatid)}/messages.txt'
        with open(messages_chat_path, 'r') as f:
            for index, message in enumerate(f):
                if start <= index <= end:
                    yield message



