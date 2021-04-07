from utilities.shared_abcs import IObserver, IObservable
from utilities.chatid import Chatid
from user.abcs import User
from message.abcs import Message
from message.message import ChatMessage
from storage.chat_storage import TextMessageStorage

message_storage=TextMessageStorage(ChatMessage)

class Chat(IObservable, IObserver):
    def __init__(self, chatid : Chatid):
        self.__chatid=chatid
        self.__all_users=[]
        self.__active_users=[]

        global message_storage
        self.__message_storage=message_storage

    def register_user(self, user: User) -> None:
        """Part of the Observer pattern (Observable)
        When a certain user wants to receive messages from this chat, this method must be called"""
        if not user in self.__active_users:
            self.__active_users.append(user)

    def remove_user(self, user : User) -> None:
        """Part of the Observer pattern (Observable)
        When a certain user for certain reason doesn't want to receive messages from this chat (at least not directly), this method must be called"""

        if user in self.__active_users:
            self.__active_users.remove(user)

    def notify_users(self, message : Message) -> None:
        """Part of the Observer pattern (Observable)
        It sends to all the users the new message"""

        for user in self.__active_users:
            user.receive_new_message(message)

    def receive_new_message(self, message : Message) -> None:
        """Part of the Observer pattern (Observer)
        It is called by a certain user and, by using a method of this class, it sends to all the users the new message
        
        Then the message is stored in the database"""

        self.notify_users(message)

        self.__message_storage.add_message(self.__chatid, message)

    def get_chatid(self):
        return self.__chatid.getValue()

class ChatProxy:
    def __init__(self, chat : Chat):
        self.__chat=chat

    def receive_new_message(self, message : Message) -> None:
        self.__chat.notify_users(message)

