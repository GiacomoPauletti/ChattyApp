from utilities.shared_abcs import IObserver, IObservable
from utilites.chatid import Chatid
from user.abcs import User


class Chat(IObservable, IObserver):
    def __init__(self, chatid : Chatid):
        self.chatid=chatid
        self.__all_users=[]
        self.__active_users=[]

    def register_active_user(self, user: User) -> None:
        """Part of the Observer pattern (Observable)
        When a certain user wants to receive messages from this chat, this method must be called"""
        self.__active_users.append(user)

    def remove_active_user(self, user : User) -> None:
        """Part of the Observer pattern (Observable)
        When a certain user for certain reason doesn't want to receive messages from this chat (at least not directly), this method must be called"""

        if user in self.__active_users:
            self.__active_users.remove(user)

    def notify_active_users(self, message : Message) -> None:
        """Part of the Observer pattern (Observable)
        It sends to all the users the new message"""

        for user in self.__active_users:
            user.receive_new_message(message)

    def receive_new_message(self, message : Message) -> None:
        """Part of the Observer pattern (Observer)
        It is called by a certain user and, by using a method of this class, it sends to all the users the new message
        
        Then the message is stored in the database"""

        self.notify_active_users(message)

        #then the message should be saved in database

    def getChatid(self):
        return self.__chatid.getValue()

