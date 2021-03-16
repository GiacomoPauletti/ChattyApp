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

    
class TextChatStorage(ChatStorage):
    def __init__(self, chats_db_path='./database/chats'):
        self.__path=chats_db_path.rstrip('/')

    def new_chat(self, chatid : Chatid):
        all_chats=os.walk(self.__path).__next__()[1] 
        if chatid in all_chats:
            return None

        new_chat_path=self.__path+f'/{chatid.to_string()}'
        os.mkdir(new_chat_path)

        open(new_chat_path + f'/{messages.txt}')
        open(new_chat_path + f'/{user_indexes.txt}') 
        open(new_chat_path + f'/{users.txt}')
                
    def add_user(self, chatid : Chatid, private_name : str):
        chat_path=self.__path + f'/{chatid.to_string()}'
        all_chats=os.walk(self.__path).__next__()[1]

        is_chat_existing=chat_path in all_chats
        if not is_chat_existing:
            return None

        users=open(chat_path, 'r').readline().split('|')
        
        is_already_added=private_name in users
        if is_already_added:
            return None

        users.append(private_name)
        open(chat_path, 'w').write('|'.join(users))

    def get_users(self, chatid : Chatid):
        chat_path=self.__path + f'/{chatid.to_string()}'
        all_chats=os.walk(self.__path).__next__()[1]

        is_chat_existing=chat_path in all_chats
        if not is_chat_existing:
            return None

        users=open(chat_path, 'r').readline().split('|')

        for user in users:
            yield users

    def get_maximum_index(self, chatid : Chatid) -> int:
        ...

    def add_message(self, chatid : Chatid, message : Message):
        ...

    def get_message_at_index(self, chatid : Chatid, index : int) -> Message:
        ...

    def get_user_index(self, chatid : Chatid, user : User) -> int:
        ...

    def increment_user_index(self, chatid : Chatid, user : User) -> None:
        ...

