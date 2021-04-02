import socket, threading

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
    def __init__(self, authorized_user_register : AuthorizedUserRegister, user_initializator):
        self.__authorized_user_register=authorized_user_register
        self.__is_listening=True
        self.__user_initializator=user_initializator

    def listen(self):
        listen_thread=threading.Thread(target=self._listen)
        listen_thread.start()

    def _listen(self):
        with socket.create_server(('', 10000)) as listener:
            print("[AuthUserListener] server is now listening")

            while self.__is_listening:
                real_client, client_address = listener.accept()    #timeout=...
                client=SocketDecorator(real_client)

                print(f"[AuthUserListener] new connection at {client_address}")

                is_authorized=self.__authorized_user_register.is_authorized_address(client_address[0])
                if is_authorized:
                    print("[AuthUserListener] connection authorized")
                    private_name=self.__authorized_user_register.pop(client_address)
                    self.__user_initializator.init_user(private_name, client, client_address)

                else:
                    print("[AuthUserListener] connection not authorized")
                    #warn the user of being not authorized
                    pass


