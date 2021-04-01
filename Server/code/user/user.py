"""import sys
sys.path.append("utilities")"""

import threading

from utilities.shared_abcs import IObserver, IObservable
from utilities.registers import AuthorizedUserRegister
from chat.abcs import Chat
from message.abcs import Message

USER_TICK_MESSAGE='tick'

def user_factory(private_name):
    return User(private_name)

def remote_user_proxy_factory(client, client_address):
    return UserRemoteProxy(client, client_address)

def init_user(private_name, client, client_address):
    server_user=user_factory(private_name)
    remote_user_proxy=remote_user_proxy_factory(client, client_address)

    user_loop=UserLoop(server_user, remote_user_proxy)
    user_loop.start()

    
class User(IObserver, IObservable):     
    def __init__(self, private_name):
        self.__chats={}
        self.__private_name=private_name
        self.__new_messages=[]


    def register_chat(self, chat : Chat) -> None:
        """Part of the Observer pattern (Observable)
        It registers the chats that eventually want to be notified, which means
        that want to know the new message"""

        self.__chats.append(chat)

    def remove_chat(self, chat : Chat ) -> None:
        """Part of the Observer Pattern (Observable)
        It removes the chats. See more info in .register_chat()"""

        if chat in self.__chats:
            self.__chats.remove(chat)

    def send_message(self, message : Message):
        """Part of the Observer pattern (Observable)
        It notifies a certain class, which means that the class will receive a user message"""

        receiver_chat=self.__chats.get(message, None)

        if receiver_chat != None:
            receiver_chat.receive_new_message(message)

    def receive_new_message(self, message : Message) -> None:
        """Part of the Observer pattern (Observer)
        It is called by a certain class and it adds a new message to the message list of this user"""

        self.__new_messages.append(message)

    def receive_unread_messages(self):
        for chat in self.__chats:
            for message in chat.send_unread_messages(self.__private_name):
                self.__messages.append(message)

    def get_new_messages(self):
        """ iterate through all messages of the user"""
        for message in self.__new_messages:
            yield message

    def pop_new_messages(self):
        """ iterate through all messages of the user and then deletes them"""
        while len(self.__new_messages):
            message=self.__new_messages[0]
            yield message
            self.__new_messages.pop(0)


class UserRemoteProxy:
    def __init__(self, client, client_address):
        self.__client=client
        self.__client_address=client_address

    def send_to_remote(self, message : Message):
        self.__client.send_with_header(message.to_string())

    def receive_from_remote(self):
        msg=self.__client.receive_with_header()
        message=msg.from_string()
        return message

class UserLoop:
    def __init__(self, server_user, user_remote_proxy, sleep=0):
        self.__user=user
        self.__user_remote_proxy=user_remote_proxy
        self.__sleep=sleep

        self.__is_active=False

    def start(self):
        loop_thread=threading.Thread(target=self._loop)
        loop_thread.start()
        
    def _loop(self):
        """Handles the messages of the remote user that must be sent a certain chat and viceversa"""

        server_user.receive_unread_messages()

        self.__is_active=True
        while self.__is_active:

            for new_message in server_user.pop_new_messages():
                user_remote_proxy.send_to_remote(new_message) 

            remote_user_message = user_remote_proxy.receive_from_remote()

            is_chat_message = remote_user_message != USER_TICK_MESSAGE
            if is_chat_message:
                #WARNING: ChatMessage è hard coded, quindi questa funzione è strictly coupled con quella classe
                message4chat=ChatMessage.from_string(remote_user_message)
                
                server_user.send_message(message4chat)


    def stop(self):
        self.__is_active=False

"""
def user_loop(server_user, user_remote_proxy, sleep=0):  #implementare sleep (il thread va in sleep tra un loop e l'altro per n tempo)
    #Handles the messages of the remote user that must be sent a certain chat and viceversa

    server_user.receive_unread_messages()

    while True:
        remote_user_message = user_remote_proxy.receive_from_remote()

        is_chat_message = remote_user_message != USER_TICK_MESSAGE
        if is_chat_message:
            #WARNING: ChatMessage è hard coded, quindi questa funzione è strictly coupled con quella classe
            message4chat=ChatMessage.from_string(remote_user_message)
            
            server_user.send_message(message4chat)

        for new_message in server_user.pop_new_messages():
            user_remote_proxy.send_to_remote(new_message) 
"""
