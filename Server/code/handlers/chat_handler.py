import threading, socket
from custom_socket.custom_socket import SocketDecorator

class ChatHandlerListener:
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
                print('[ChatHandlerServer] new connection')
                real_client, address=server.accept()
                client=SocketDecorator(real_client)

                self.__chat_handler.handle(client, address)
    

    def stop(self):
        self.__is_listening=False

class ChatHandler:
    def __init__(self, user_message_class):
        self.__UserMessage=user_message_class
        self.__client_action_map={'create_chat':self.new_chat, 'leave_chat':self.leave_chat, 'join_chat'.self.join_chat, 'add_user_to_chat':self.add_user_to_chat}

    def handle(self, client, client_address):
        handle_thread=threading.Thread(target=self._handle, args=(client, client_address))
        handler_thread.start()

    def _handle(self, client, client_address):
        while True:
            try:
                msg=client.recv_with_header()
                msg=self.__UserMessage.from_string(msg)

                self.__client_action_map[msg.get_action()](client=client, client_address=client_address, msg=msg)
            except:
                pass

    def new_chat(self, client, client_address, msg):
        ...

    def leave_chat(self, client, client_address, msg):
        ...

    def join_chat(self, client, client_address, msg):
        ...

    def add_user_to_chat(self, client, client_address, msg):
        ...


