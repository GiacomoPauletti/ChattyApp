import socket, threading

from utilities.registers import AuthorizedUserRegister
from handlers.access_handler import AccessHandler 
from custom_socket.custom_socket import SocketDecorator

class UnauthUserServer:
    def __init__(self, access_handler : AccessHandler, timeout=30):
        self.__access_handler=access_handler 
        self.__is_listening=False
        self.__timeout=timeout

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
                real_client.settimeout(self.__timeout)
                client=SocketDecorator(real_client)

                print("[UnauthUserServer] new connection")

                self.__access_handler.handle(client=client, client_address=client_address)

    def stop(self):
        self.__is_listening=False

    def set_timeout(self, timeout):
        self.__timeout=timeout

    def get_timeout(self):
        return self.__timeout


class AuthUserServer:
    def __init__(self, authorized_user_register : AuthorizedUserRegister, user_initializator, timeout=600):
        self.__authorized_user_register=authorized_user_register
        self.__is_listening=False
        self.__timeout=timeout

        self.__user_initializator=user_initializator
        self.__user_initializator.set_timeout(self.__timeout)


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
                real_client.settimeout(self.__timeout)

                print(f"[AuthUserServer] new connection at {client_address}")

                is_authorized=self.__authorized_user_register.is_authorized_address(client_address[0])
                if is_authorized:
                    print("[AuthUserServer] connection authorized")
                    private_name=self.__authorized_user_register.get(client_address[0])

                    self.__user_initializator.init_user(private_name, client, client_address)

                else:
                    print("[AuthUserServer] connection not authorized")
                    #warn the user of being not authorized
                    pass
    def stop(self):
        self.__is_listening=False

    def set_timeout(self, timeout):
        self.__timeout=timeout

    def get_timeout(self):
        return self.__timeout

