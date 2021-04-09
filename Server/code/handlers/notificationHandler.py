import socket, threading
from custom_socket.custom_socket import SocketDecorator

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
                real_client, client_address.accept()

                client=SocketDecorator(real_client)
                self.__notification_handler.handle(client, client_address)

            
class NotificationHandler:
    def __init__(self, user_message_class, answer_message_class, notification_storage):
        self.__UserMessage=user_message_class
        self.__AnswerMessage=answer_message_class
        self.__notification_storage=notification_storage

        self.__

    def handle(self, client, client_address):
        listen_thread=threading.Thread(target=self._handle, args=(client, client_address))
        listen_thread.start()
        
    def _handle(self, client, client_address):



    
