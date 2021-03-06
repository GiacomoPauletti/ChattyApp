import socket
from user.user import user_initializator
from utilities.registers import AuthorizedUserRegister

class UnaccessedUserListener:
    def __init__(self):
        ...

    def listen(self):
        with socket.create_server(('', 8000)) as listener:
            client, client_address = listener.accept()    #timeout=...

            #create new User
            #make the UserActivityHandler (or whatever is the one which login or register the user) listen for the new user

class AccesseduserListener:
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

