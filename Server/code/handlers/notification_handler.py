import socket, threading
from custom_socket.custom_socket import SocketDecorator
from storage.user_storage import TextNotificationStorage
import message.message as msg

def text_notification_storage_factory(user_message_class=msg.NotificationRequestMessage, answer_message_class=NotificationAnswerMessage, auth_user_register):
    notification_storage=TextNotificationStorage()
    return NotificationHandler(user_message_class, answer_message_class, auth_user_register, notification_storage)

class NotificationServer:
    def __init__(self, notification_handler):
        self.__is_listening=False
        self.__notification_handler=notification_handler
        self.__address=('', 12000)

    def listen(self):
        listen_thread=threading.Thread(target=self._listen)
        listen_thread.start()

    def _listen(self):
        if self.__is_listening:
            return None

        with socket.create_server(self.__address) as real_server:
            server=SocketDecorator(real_server)

            self.__is_listening=True
            while self.__is_listening:
                real_client, client_address = real_server.accept()

                print('[NotificationServer] new connection')

                client=SocketDecorator(real_client)
                self.__notification_handler.handle(client, client_address)

            
class NotificationHandler:
    def __init__(self, user_message_class=msg.NotificationRequestMessage, answer_message_class=NotificationAnswerMessage, auth_user_register, notification_storage):
        self.__auth_user_register=auth_user_register
        self.__UserMessage=user_message_class
        self.__AnswerMessage=answer_message_class
        self.__notification_storage=notification_storage

        self.__client_action_map={'get':self.get}  #per ora un utente può solo ricevere i suoi messaggi

    def handle(self, client, client_address):
        listen_thread=threading.Thread(target=self._handle, args=(client, client_address))
        listen_thread.start()
        
    def _handle(self, client, client_address):

        while True:

            message=client.recv_with_header()
            message=self.__UserMessage.from_string(message)
            print(f'[NotificationHandler] new message')

            self.__client_action_map[message.get_action()](client, client_address, message)

    def get(self, client, client_address, msg):
        client_address=client_address[0] if type(client_address) == tuple else client_address
        real_private_name=self.__auth_user_register.get(client_address)

        registered_address = real_private_name
        if  not registered_address:
            print('[NotificationHandler] user not authorized to retrieve notifications')
            answer_message=self.__AnswerMessage(answer='failed', content='not authorized')
            client.send_with_header(str(answer_message))
            return None

        sender_private_name=msg.get_sender()
        different_names = real_private_name != sender_private_name
        if different_names:
            print('[NotificationHandler] user sent a different name from the one which is saved')
            answer_message=self.__AnswerMessage(answer='failed', content='wrong private_name')
            client.send_with_header(str(answer_message))
            return None
        

        for notification in self.__notification_storage.pop(sender_private_name):
            answer_message=self.__AnswerMessage(answer='notification', content=notification)
            client.send_with_header(str(answer_message))

        end_message=self.__AnswerMessage(answer='END', content='END')
        client.send_with_header(str(end_message))
        

    



    
