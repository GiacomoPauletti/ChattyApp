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
    def __init__(self, address_register, user_message_class, answer_message_class, notification_storage):
        self.__address_register=address_register
        self.__UserMessage=user_message_class
        self.__AnswerMessage=answer_message_class
        self.__notification_storage=notification_storage

        self.__client_action_map={'get':self.get}  #per ora un utente può solo ricevere i suoi messaggi

    def handle(self, client, client_address):
        listen_thread=threading.Thread(target=self._handle, args=(client, client_address))
        listen_thread.start()
        
    def _handle(self, client, client_address):

        while True:

            try:
                msg=client.recv_with_header()
                msg=self.__UserMessage.from_string(msg)

                self.__client_action_map[msg.get_action()](client, client_address, msg)
            except:
                pass

    def get(self, client, client_address, msg):
        real_private_name=self.__address_register.get(client_address, None)

        registered_address = real_private_name
        if  not registered_address:
            answer_message=self.__AnswerMessage(action='failed', content='not authorized')
            client.send_with_header(str(answer_message))
            return None

        sender_private_name=msg.get_sender()
        different_names = real_private_name != sender_private_name
        if different_names:
            answer_message=self.__AnswerMessage(action='failed', content='wrong private_name')
            client.send_with_header(str(answer_message))
            return None
        

        for notification in self.__notification_storage.pop(private_name):
            answer_message=self.__AnswerMessage(action='notification', content=notification)
            client.send_with_header(str(answer_message))

        end_message=self.__AnswerMessage(action='END', content='END')
        client.send_with_header(str(end_message))
        

    



    
