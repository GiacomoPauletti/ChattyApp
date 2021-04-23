import threading, time

from utilities.shared_abcs import IObserver, IObservable
from utilities.registers import AuthorizedUserRegister
from chat.abcs import Chat
from message.abcs import Message
import message.message as msg
from storage.user_storage import TextUserChatStorage
from utilities.chatid import Chatid

USER_TICK_MESSAGE='tick'

def user_factory(private_name):
    return User(private_name)

def remote_user_proxy_factory(client, client_address):
    return UserRemoteProxy(client, client_address)

def get_text_user_initializator(active_user_register, active_chat_register):
    return UserInitializator(active_user_register, active_chat_register, TextUserChatStorage())

class UserInitializator:
    def __init__(self, active_user_register, active_chat_register, user_chat_storage):
        self.__active_user_register=active_user_register
        self.__active_chat_register=active_chat_register
        self.__user_chat_storage=user_chat_storage

    def init_user(self, private_name, client, client_address):
        server_user=user_factory(private_name)
        remote_user_proxy=remote_user_proxy_factory(client, client_address)

        self._init_user_chats(server_user)

        self.__active_user_register.add(private_name, server_user)

        user_loop=UserLoop(server_user, remote_user_proxy)
        user_loop.start()

    def _init_user_chats(self, server_user):
        private_name=server_user.get_private_name()
        for chatid in self.__user_chat_storage.get(private_name):
            chat_obj=self.__active_chat_register.get(chatid, force=True)
            chat_obj.register_user(server_user)
            server_user.register_chat(str(chatid), chat_obj)

    
class User(IObserver, IObservable):     
    def __init__(self, private_name):
        self.__chats={}
        self.__private_name=private_name
        self.__new_messages=[]
        self.__old_messages=[]

    def get_private_name(self):
        return self.__private_name

    def register_chat(self, chatid, chat : Chat) -> None:
        """Part of the Observer pattern (Observable)
        It registers the chats that eventually want to be notified, which means
        that want to know the new message"""

        self.__chats[str(chatid)]=chat

    def remove_chat(self, chatid : Chatid ) -> None:
        """Part of the Observer Pattern (Observable)
        It removes the chats. See more info in .register_chat()"""

        self.__chats.pop(chatid, None)

    def send_message(self, message : Message):
        """Part of the Observer pattern (Observable)
        It notifies a certain class, which means that the class will receive a user message"""

        chatid=str(message.get_chat())
        receiver_chat=self.__chats.get(chatid, None)

        if receiver_chat != None:
            receiver_chat.receive_new_message(message)

    def receive_new_message(self, message : Message) -> None:
        """Part of the Observer pattern (Observer)
        It is called by a certain class and it adds a new message to the new messages list of this user"""

        self.__new_messages.append(message)

    def get_new_messages(self):
        """ iterate through all new messages of the user"""
        for message in self.__new_messages:
            yield message

    def pop_new_messages(self):
        """ iterate through all new messages of the user and then deletes them"""
        while len(self.__new_messages):
            message=self.__new_messages[0]
            yield message
            self.__new_messages.pop(0)

    def receive_old_message(self, message : Message) -> None:
        """Part of the Observer pattern (Observer)
        It is called by a certain class and it adds an old message to the old messages list of this user"""

        self.__old_messages.append(message)

    def get_old_messages(self):
        """ iterate through all old messages of the user"""
        for message in self.__old_messages:
            yield message

    def pop_old_messages(self):
        """ iterate through all old messages of the user and then deletes them"""
        while len(self.__old_messages):
            message=self.__old_messages[0]
            yield message
            self.__old_messages.pop(0)

    def receive_unread_messages(self):
        for chat in self.__chats.values():
            chat.send_unread_messages(self.__private_name)

    def delete(self):
        print('[User] user deleted')

        for chat in self.__chats.values():
            chat.remove_user(self)

        del self

    def __del__(self):
        print('[User] user totally deleted')


class UserRemoteProxy:
    def __init__(self, client, client_address):
        self.__client=client
        self.__client_address=client_address

    def send_to_remote(self, message : Message):
        self.__client.send_with_header(message)

    def receive_from_remote(self):
        msg=self.__client.recv_with_header()
        message=str(msg)
        return message

    def close(self):
        self.__client.close()

class UserLoop:
    def __init__(self, server_user, user_remote_proxy, sleep=0, chat_request_message_class=msg.ChatRequestMessage, chat_message_class=msg.ChatMessage, timeout=60):
        self.__server_user=server_user
        self.__user_remote_proxy=user_remote_proxy
        self.__sleep=sleep
        self.__ChatRequestMessage=chat_request_message_class
        self.__ChatMessage=chat_message_class

        self.__timeout=timeout

        self.__user_action_map={'chat':self.chat, 'tick':self.tick, 'disconnect':self.disconnect}

        self.__is_active=False
        self.__timeout=10

    def start(self):
        loop_thread=threading.Thread(target=self._loop)
        loop_thread.start()
        
    def _loop(self):
        """Handles the messages of the remote user that must be sent a certain chat and viceversa"""

        self.__start_=time.time() 

        self.__server_user.receive_unread_messages()

        self.__is_active=True
        threading.Thread(target=self._listening_loop).start()
        while self.__is_active:
            now=time.time()
            if self.__start_ + self.__timeout < now:
                print('[UserLoop] timed out')

            remote_user_message = self.__user_remote_proxy.receive_from_remote()

            user_request=self.__ChatRequestMessage.from_string(remote_user_message)

            if not user_request:
                continue

            self.__user_action_map[user_request.get_action()](user_request)
        return None

    def _listening_loop(self):
        while self.__is_active:

            now=time.time()
            if now - self.__start_ >= self.__timeout:
                #+ send disconnection message to user
                print('[UserLoop] timed out')
                self.__user_remote_proxy.close()
                self.stop()
                return None

            for new_message in self.__server_user.pop_new_messages():
                answer_message=msg.ChatAnswerMessage(answer='new_message', message=new_message)
                self.__user_remote_proxy.send_to_remote(answer_message) 

            for old_message in self.__server_user.pop_old_messages():
                answer_message=msg.ChatAnswerMessage(answer='old_message', message=old_message)
                self.__user_remote_proxy.send_to_remote(answer_message) 

            time.sleep(3)



    def stop(self):
        self.__is_active=False

    def chat(self, user_request):
        chat_message=user_request.get_message()
        self.__server_user.send_message(chat_message)

    def tick(self, user_request):
        self.__start_=time.time()

    def disconnect(self, user_request):
        print('[UserLoop] client disconnected')
        #ora si deve anche "distruggere" le classi User e UserProxy quivi usate

        self.__server_user.delete()
        del self.__server_user

        self.__user_remote_proxy.close()
        del self.__user_remote_proxy

        self.stop()
        del self


    def tick(self, client, client_address, msg):
        self.__start_=time.time()


        


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
