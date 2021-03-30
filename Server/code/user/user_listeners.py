import socket, threading

from user.user import user_initializator
from utilities.registers import AuthorizedUserRegister
from handlers.access_handler import AccessHandler 
from custom_socket.custom_socket import SocketDecorator

class UnauthUserListener:
    def __init__(self, access_handler : AccessHandler):
        self.__access_handler=access_handler 
        self.__is_listening=True

    def listen(self):
        listen_thread=threading.Thread(target=self._listen)
        listen_thread.start()

    def _listen(self):
        with socket.create_server(('', 8000)) as listener:
            print("[UnauthUserListener] server is now listening")

            while self.__is_listening:
                real_client, client_address = listener.accept()    #timeout=...
                client=SocketDecorator(real_client)

                print("[UnauthUserListener] new connection")

                self.__access_handler.handle(client=client, client_address=client_address)


class AuthUserListener:
    def __init__(self, authorized_user_register : AuthorizedUserRegister):
        self.__authorized_user_register=authorized_user_register
        self.__is_listening=True

    def listen(self):
        listen_thread=threading.Thread(target=self._listen)
        listen_thread.start()

    def _listen(self):
        with socket.create_server(('', 10000)) as listener:
            print("[AuthUserListener] server is now listening")

            while self.__is_listening:
                real_client, client_address = listener.accept()    #timeout=...
                client=SocketDecorator(real_client)

                print("[AuthUserListener] new connection")

                is_authorized=self.__authorized_user_register.is_authorized_address(client_address)
                if is_authorized:
                    private_name=self.__authorized_user_register.get_name_by_address(client_address)
                    user_initializator(private_name, client, client_address)
                else:
                    #warn the user of being not authorized
                    pass


