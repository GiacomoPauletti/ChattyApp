import socket, threading

from utilities.registers import AuthorizedUserRegister
from handlers.access_handler import AccessHandler 
from custom_socket.custom_socket import SocketDecorator

class UnauthUserServer:
    def __init__(self, access_handler : AccessHandler):
        self.__access_handler=access_handler 
        self.__is_listening=False

    def listen(self):
        listen_thread=threading.Thread(target=self._listen)
        listen_thread.start()

    def _listen(self):
        with socket.create_server(('', 8000)) as real_server:
            print("[UnauthUserServer] server is now listening")

            server=SocketDecorator(real_server)

            self.__is_listening=True
            while self.__is_listening:
                real_client, client_address = server.accept()    #timeout=...
                client=SocketDecorator(real_client)

                print("[UnauthUserServer] new connection")

                self.__access_handler.handle(client=client, client_address=client_address)

    def stop(self):
        self.__is_listening=False


class AuthUserServer:
    def __init__(self, authorized_user_register : AuthorizedUserRegister, user_initializator):
        self.__authorized_user_register=authorized_user_register
        self.__is_listening=False
        self.__user_initializator=user_initializator

    def listen(self):
        listen_thread=threading.Thread(target=self._listen)
        listen_thread.start()

    def _listen(self):
        with socket.create_server(('', 10000)) as real_server:
            print("[AuthUserServer] server is now listening")

            server=SocketDecorator(real_server)

            self.__is_listening=True
            while self.__is_listening:
                real_client, client_address = server.accept()    #timeout=...
                client=SocketDecorator(real_client)

                print(f"[AuthUserServer] new connection at {client_address}")

                is_authorized=self.__authorized_user_register.is_authorized_address(client_address[0])
                if is_authorized:
                    print("[AuthUserServer] connection authorized")
                    private_name=self.__authorized_user_register.get(client_address)
                    self.__user_initializator.init_user(private_name, client, client_address)

                else:
                    print("[AuthUserServer] connection not authorized")
                    #warn the user of being not authorized
                    pass
    def stop(self):
        self.__is_listening=False


