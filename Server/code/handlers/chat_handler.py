import threading, socket, time
from custom_socket.custom_socket import SocketDecorator
from storage.chat_storage import TextChatStorageFactory
from storage.user_storage import TextNotificationStorage
import message.message as msg

def text_chat_handler_factory(auth_user_register, active_chat_register, user_message_class=msg.ChatHandlingRequestMessage, answer_message_class=msg.ChatHandlingAnswerMessage, notification_message_class=msg.NotificationMessage):
    tcsf=TextChatStorageFactory()
    chat_storage_facade=tcsf.get_facade()
    chat_user_storage=tcsf.get_chat_user_storage()
    notification_storage=TextNotificationStorage(notification_message_class)

    return ChatHandler(user_message_class, answer_message_class, notification_message_class, active_chat_register, auth_user_register, chat_storage_facade, chat_user_storage, notification_storage)


class ChatHandlerServer:
    def __init__(self, chat_handler):
        self.__address=('', 11000)
        self.__is_listening=False
        self.__chat_handler=chat_handler

    def listen(self):
        listen_thread=threading.Thread(target=self._listen)
        listen_thread.start()

    def _listen(self):
        with socket.create_server(self.__address) as real_server:
            print('[ChatHandlerServer] server is now listening')
            server=SocketDecorator(real_server)

            self.__is_listening=True
            while self.__is_listening:
                real_client, address=server.accept()
                print('[ChatHandlerServer] new connection')
                client=SocketDecorator(real_client)

                self.__chat_handler.handle(client, address)
    

    def stop(self):
        self.__is_listening=False

class ChatHandler:
    def __init__(self, user_message_class, answer_message_class, notification_message_class, active_chat_register, auth_user_register, chat_storage_facade, chat_user_storage, notification_storage):
        self.__UserMessage=user_message_class
        self.__AnswerMessage=answer_message_class
        self.__NotificationMessage=notification_message_class

        self.__active_chat_register=active_chat_register
        self.__auth_user_register=auth_user_register
        
        self.__chat_storage_facade=chat_storage_facade
        self.__chat_user_storage=chat_user_storage
        self.__notification_storage=notification_storage

        self.__client_action_map={'create_chat':self.create_chat, 'leave_chat':self.leave_chat, 'join_chat':self.join_chat, 'add_users':self.add_users, 'disconnect':self.disconnect, 'tick':self.tick}
        self.__active_clients={}
        self.__timeout=60

    def handle(self, client, client_address):
        handle_thread=threading.Thread(target=self._handle, args=(client, client_address))
        handle_thread.start()

    def _handle(self, client, client_address):

        start=time.time()
        self.__active_clients[client_address[0]]=start

        while client_address[0] in self.__active_clients:
            now=time.time()
            if start+self.__timeout < now:
                print('[ChatHandler] timed out')
                client.close()
                self.__active_clients.pop(client_address[0])
                return None

            try:
                msg=client.recv_with_header()
                msg=self.__UserMessage.from_string(msg)

            except:
                pass

            self.__client_action_map[msg.get_action()](client=client, client_address=client_address, msg=msg)

    def create_chat(self, client, client_address, msg):
        #generazione di un nuovo chatid (forse) al posto di questo commento

        private_name=self.__auth_user_register.get(client_address[0])
        if not private_name:
            client.send_with_header(self.__AnswerMessage(answer='failed', content='not authorized'))    
            return False

        chatid=msg.get_chat()
        if self.__chat_storage_facade.new_chat(chatid):
            print('[ChatHandler] new chat created')
            #essendo stata appena creata, la chat non può essere nel registro, così chiamare il metodo .get() mi crea l'oggetto e me lo aggiunge al registro
            chat_obj=self.__active_chat_register.get(chatid)

            self.join_chat(client, client_address, msg, mute=True)
            self.add_users(client, client_address, msg)

            client.send_with_header(self.__AnswerMessage(answer='success', content=f'created {chatid}'))
            return True
        else:
            client.send_with_header(self.__AnswerMessage(answer='failed', content=f'{chatid} already existing'))     
            return False
        
            

    def leave_chat(self, client, client_address, msg):
        chatid=msg.get_chat()
        private_name=self.__auth_user_register.get(client_address[0])

        if not private_name in self.__chat_user_storage.get_users(chatid):
            return True

        if self.__chat_user_storage.remove_user(chatid, private_name):
            client.send_with_header(self.__AnswerMessage(answer='success', content=f'left {chatid}'))
            return True
        else:
            client.send_with_header(self.__AnswerMessage(answer='failed', content=f'unable to leave {chatid}'))
            return False

    def join_chat(self, client, client_address, msg, mute=False):
        chatid=msg.get_chat()
        private_name=self.__auth_user_register.get(client_address[0])

        if private_name in self.__chat_user_storage.get_users(chatid):
            return True

        if self.__chat_storage_facade.add_user(chatid, private_name):
            if not mute:
                client.send_with_header(self.__AnswerMessage(answer='success', content=f'joined {chatid}'))
            return True
        else:
            if not mute:
                client.send_with_header(self.__AnswerMessage(answer='failed', content=f'unable to change {chatid}'))
            return False


    def add_users(self, client, client_address, msg):
        chatid=msg.get_chat()
        private_name=self.__auth_user_register.get(client_address[0])

        for user in msg.get_users():
            if user in self.__chat_user_storage.get_users(chatid):
                continue

            self.__chat_storage_facade.add_user(chatid, user)

            notification_message=self.__NotificationMessage.from_string(f'{private_name}|{msg.get_users_str()}|added to {chatid}')
            self.__notification_storage.add(user, notification_message)

    def disconnect(self, client, client_address, msg):
        print('[ChatHandler] client disconnected')
        self.__active_clients.pop(client_address[0])
        client.close()

    def tick(self, client, client_address, msg):
        if client_address[0] in self.__active_clients.keys():
            self.__active_clients[client_address[0]]=time.time()

        


