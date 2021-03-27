from socket import socket
import threading

from message.abcs import Message
from storage.abcs import UserLogger, UserRegister
import storage.accessing as accessing
from user.abcs import User
from utilities.registers import AuthorizedUserRegister

#si può creare una classe socket personalizzata che possiede anche il
#metodo "socket.recv()"

def text_access_handler_factory(user_message, access_answer_message, authorized_user_register, users_database_path='./database/users'):
    tuaf=accessing.TextUserAccesserFactory(users_database_path)
    user_logger=tuaf.get_logger()
    user_register=tuaf.get_register()

    return AccessHandler(user_logger, user_register, user_message, access_answer_message, authorized_user_register)

class AccessHandler:
    def __init__(self, user_logger : UserLogger, user_register : UserRegister, user_message : Message, access_answer_message : Message, authorized_user_register : AuthorizedUserRegister):
        self.__user_logger=user_logger
        self.__user_register=user_register

        self.__UserMessage=user_message  #per ora AccessMessage
        self.__AccessAnswerMessage=access_answer_message #per ora AccessAnswerMessage

        self.__authorized_user_register=authorized_user_register

        self.__access_type_map={'login':self.login, 'register':self.register, 'disconnect':self.disconnect}

    def handle_access(self, client : socket, client_address : tuple) -> None:

        handle_access_thread=threading.Thread(target=self._handle_access, args=(client, client_address))
        handle_access_thread.start()

    def _handle_access(self, client : socket, client_address : tuple) -> None:
        """AccessHandler._handler_access(self, client : socket, client_address : tuple, msg : Message) -> User

        WHAT IT DOES
        It handle login/registration requests of a specific user by calling the appropriate methods of this class.
        Until the user hasn't logged in/registered it and if it hasn't disconnected, it will keep waiting for user requests.
        See AccessHandler.login and AccessHandler.register for more info.
        """

        while True:
            
            try:
                msg=client.recv_with_header()
                msg=self.__UserMessage.from_string(message)

                has_accessed=self.__access_type_map[msg.type](client=client, client_address=address, msg=msg)
                if has_accessed:
                    self.__authorized_user_register.add(client_address, msg.get_private_name())
                    print(f'[AccessHandler] the user {msg.get_private_name()} has accessed')
                    break
                print(f'[AccessHandler] the user {msg.get_private_name()} has NOT accessed')
            except:
                continue

    def login(self, client : socket, client_address : tuple, msg : Message):
        """AccessHandler.login(self, client : socket,, client_address : tuple, msg : Message) -> bool
        
        WHAT IT DOES
        It is an interface between the client (remote) and the UserLogger.
        If the login isn't successfull, an error descriptions is sent back to the client
        See UserLogger for more informations about the user login"""
        
        has_logged_correctly=self.__user_logger.login(private_name=msg.get_private_name(), password=msg.get_password())

        if has_logged_correctly:
            answer_msg=self.__AccessAnswerMessage(answer='success')

        else:
            error=self.__user_logger.get_error()
            answer_msg=self.__AccessAnswerMessage(answer='failed', error=error)

        client.send_with_header(answer_msg.to_string())
        return has_logged_correctly

    def register(self, client : socket, client_address : tuple, msg : Message) -> bool:
        """AccessHandler.register(self, client : socket,, client_address : tuple, msg : Message) -> bool
        
        WHAT IT DOES
        It is an interface between the client (remote) and the RemoteLogger.
        If the registration isn't successfull, an error descriptions is sent back to the client
        See UserLogger for more informations about the user registration"""

        has_registered_correctly=self.__user_register.register(private_name=msg.get_private_name(), password=msg.get_password(), email=msg.get_email())

        if has_registered_correctly:
            answer_msg=self.__AccessAnswerMessage(answer='success')
        else:
            error=self.__user_register.get_error()
            answer_msg=self.__AccessAnswerMessage(answer='failed', error=error)

        client.send_with_header(answer_msg.to_string())
        return has_registered_correctly

    def disconnect(self, *args, **kwargs) -> bool:
        """AccessHandler.disconnect(self, *args, **kwargs) -> bool
        
        WHAT IT DOES
        It stops the waiting-request loop after a disconnection message of the User
        """

        return True
        
