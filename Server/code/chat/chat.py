from utilities.shared_abcs import IObserver, IObservable
from utilities.chatid import Chatid
from user.abcs import User
from message.abcs import Message
from message.message import ChatMessage
from storage.chat_storage import TextMessageStorage, TextChatUserStorage

message_storage=TextMessageStorage(ChatMessage)


class Chat(IObservable, IObserver):
    def __init__(self, chatid : Chatid, message_storage=TextMessageStorage(ChatMessage), chat_user_storage=TextChatUserStorage()):
        self.__chatid=chatid
        self.__all_users=[]
        self.__active_users=[]

        self.__message_storage=message_storage
        self.__chat_user_storage=chat_user_storage

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
            private_name=user.get_private_name()
            self.__chat_user_storage.increment_user_index(str(self.__chatid), private_name)

            if private_name != message.get_sender():
                user.receive_new_message(message)

    def receive_new_message(self, message : Message) -> None:
        """Part of the Observer pattern (Observer)
        It is called by a certain user and, by using a method of this class, it sends to all the users the new message
        
        Then the message is stored in the database"""

        self.notify_users(message)

        self.__message_storage.add_message(self.__chatid, message)

    def send_unread_messages(self, private_name):
        is_active=False
        for user in self.__active_users:
            if user.get_private_name() == private_name: 
                is_active=True
                receiver=user
                break

        if not is_active:
            print('[Chat] user is not active')
            return False

        receiver_index=self.__chat_user_storage.get_user_index(self.get_chatid(), private_name)
        for message in self.__message_storage.get_messages(self.get_chatid(), receiver_index):
            receiver.receive_new_message(message)
            self.__chat_user_storage.increment_user_index(self.get_chatid(), private_name)

    def get_chatid(self):
        return str(self.__chatid)

class ChatProxy:
    def __init__(self, chat : Chat):
        self.__chat=chat

    def receive_new_message(self, message : Message) -> None:
        self.__chat.notify_users(message)

