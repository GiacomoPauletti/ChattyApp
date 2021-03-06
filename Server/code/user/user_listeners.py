import socket
from user.user import user_initializator
from utilities.registers import AuthorizedUserRegister
from handlers.access_handler import AccessHandler 

class UnaccessedUserListener:
    def __init__(self, access_handler : AccessHandler):
        self.__access_handler=access_handler 
    def listen(self):
        with socket.create_server(('', 8000)) as listener:
            client, client_address = listener.accept()    #timeout=...

            self.__access_handler.handle_access(client=client, client_address=client_address)

class AccessedUserListener:
    def __init__(self, authorized_user_register : AuthorizedUserRegister):
        self.__authorized_user_register=authorized_user_register

    def listen(self):
        with socket.create_server(('...', 10000)) as listener:
            client, client_address = listener.accept()

            is_authorized=self.__authorized_user_register.is_authorized_address(client_address)
            if is_authorized:
                private_name=self.__authorized_user_register.get_name_by_address(client_address)
                user_initializator(private_name, client, client_address)
            else:
                #warn the user of being not authorized
                pass

