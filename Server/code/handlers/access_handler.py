from socket import socket
import threading

from message.abcs import Message
import message.message as msg
from storage.abcs import UserLogger, UserRegister
import storage.accessing as accessing
from utilities.registers import AuthorizedUserRegister

#si può creare una classe socket personalizzata che possiede anche il
#metodo "socket.recv()"

def text_access_handler_factory(authorized_user_register, users_database_path='./database/users', user_message_class=msg.AccessRequestMessage, answer_message_class=msg.AccessAnswerMessage):
    tuaf=accessing.TextUserAccesserFactory(users_database_path)
    user_logger=tuaf.get_logger()
    user_registrator=tuaf.get_registrator()

    return AccessHandler(user_logger=user_logger, user_registrator=user_registrator, user_message_class=user_message_class, answer_message_class=answer_message_class, authorized_user_register=authorized_user_register)

class AccessHandler:
    def __init__(self, user_logger : UserLogger, user_registrator : UserRegister, user_message_class, answer_message_class, authorized_user_register : AuthorizedUserRegister):
        self.__user_logger=user_logger
        self.__user_registrator=user_registrator

        self.__UserMessage=user_message_class  
        self.__AnswerMessage=answer_message_class 

        self.__authorized_user_register=authorized_user_register

        self.__access_type_map={'login':self.login, 'register':self.register, 'disconnect':self.disconnect}

    def handle(self, client : socket, client_address : tuple) -> None:

        handle_access_thread=threading.Thread(target=self._handle, args=(client, client_address))
        handle_access_thread.start()

    def _handle(self, client : socket, client_address : tuple) -> None:
        """AccessHandler._handler_access(self, client : socket, client_address : tuple, msg : Message) -> User

        WHAT IT DOES
        It handle login/registration requests of a specific user by calling the appropriate methods of this class.
        Until the user hasn't logged in/registered it and if it hasn't disconnected, it will keep waiting for user requests.
        See AccessHandler.login and AccessHandler.register for more info.
        """

        handling=True
        while handling:
            
            try:
                msg=client.recv_with_header()
                msg=self.__UserMessage.from_string(msg)

                has_accessed=self.__access_type_map[msg.get_action()](client=client, client_address=client_address, msg=msg)
                if has_accessed:
                    self.__authorized_user_register.add(client_address[0], msg.get_private_name())
                    print(f'[AccessHandler] the user {msg.get_private_name()} at {client_address} has accessed')
                    client.close()
                    handling=False
                    return True
                print(f'[AccessHandler] the user {msg.get_private_name()} has NOT accessed')
            except Exception as e:
                #print(f'[AccessHandler] error: {e}')
                continue

    def login(self, client : socket, client_address : tuple, msg : Message):
        """AccessHandler.login(self, client : socket,, client_address : tuple, msg : Message) -> bool
        
        WHAT IT DOES
        It is an interface between the client (remote) and the UserLogger.
        If the login isn't successfull, an error descriptions is sent back to the client
        See UserLogger for more informations about the user login"""
        
        has_logged_correctly=self.__user_logger.login(private_name=msg.get_private_name(), password=msg.get_password())

        if has_logged_correctly:
            answer_msg=self.__AnswerMessage(answer='success')

        else:
            error=self.__user_logger.get_error()
            answer_msg=self.__AnswerMessage(answer='failed', error=error)

        client.send_with_header(str(answer_msg))
        return has_logged_correctly

    def register(self, client : socket, client_address : tuple, msg : Message) -> bool:
        """AccessHandler.register(self, client : socket,, client_address : tuple, msg : Message) -> bool
        
        WHAT IT DOES
        It is an interface between the client (remote) and the RemoteLogger.
        If the registration isn't successfull, an error descriptions is sent back to the client
        See UserLogger for more informations about the user registration"""

        has_registered_correctly=self.__user_registrator.register(private_name=msg.get_private_name(), password=msg.get_password(), email=msg.get_email())

        if has_registered_correctly:
            answer_msg=self.__AnswerMessage(answer='success')
        else:
            error=self.__user_registrator.get_error()
            answer_msg=self.__AnswerMessage(answer='failed', error=error)

        client.send_with_header(answer_msg)
        return has_registered_correctly

    def disconnect(self, *args, **kwargs) -> bool:
        """AccessHandler.disconnect(self, *args, **kwargs) -> bool
        
        WHAT IT DOES
        It stops the waiting-request loop after a disconnection message of the User
        """

        return True
        
