from socket import socket
import message
from message import Message
import storage
from storage import UserLogger, UserRegister
from user import User, UserFactory
"""
class ActiveUserList:
    def __init__(self):
        self.__active_users={}
    
    def add_user(self, user : User, address : str):
        self.__active_users[address]=user

    def remove_user_by_address(self, address):
        self.__active_users.pop(address, False)

    def is_address_active(self, address : str):
        return address in self.__active_users.keys()
    
    def is_user_active(self, user : User):
        return user in self.__active_users.values()
        
    def find_user_by_address(self, address : str):
        return self.__active_users.get(address, None)

    def find_address_by_user(self, user : User):
        for (current_address, current_user) in self.__active_users:
            if current_user == user:
                return current_address
"""

class AccessHandler:
    def __init__(self, user_logger : UserLogger, user_register : UserRegister, user_factory : UserFactory, user_message : Message, access_answer_message : Message):
        self.__UserLogger=user_logger
        self.__UserRegister=user_register
        self.__UserFactory=user_factory

        self.__UserMessage=user_message  #per ora AccessMessage
        self.__AccessAnswerMessage=access_answer_message #per ora AccessAccessAnswerMessage

        self.__access_type_map={'autologin':self.login, 'register':self.register}


    def handle_access(self, client : socket, client_address : tuple) -> User:
        #si può creare una classe socket personalizzata che possiede anche il
        #metodo "socket.recv()"

        while True:
            msg=client.recvwh()
            msg=self.__UserMessage.from_string(message)

            has_accessed=self.__access_type_map[msg.type](client=client, client_address=address, msg=msg)
            if has_accessed:
                break

        disconnection_message=self.__AccessAnswerMessage(answer='disconnecting')
        
        
        user=self.__UserFactory(client, address)
        return user

    def autologin(self, client : socket, address : tuple, msg : Message) -> bool:
        return True

    def register(self, client : socket, client_address : tuple, msg : Message) -> bool:
        
        has_registered_correctly=self.__UserRegister.register(user_private_name=msg.user_private_name, user_password=msg.user_password)

        if has_registered_correctly:
            answer_msg=self.__AccessAnswerMessage(answer='success')
        else:
            error_info=self.__UserLogger.getErrorDescription()
            answer_msg=self.__AccessAnswerMessage(answer='error', error_info=error_info)

        client.sendwh(answer_msg.to_string())
        return has_registered_correctly


    """def login(self, client : socket, client_address : tuple, msg : Message):
        
        has_logged_correctly=self.__UserLogger.login(user_private_name=msg.user_private_name, user_password=msg.user_password)

        if has_logged_correctly:
            answer_msg=self.__AccessAnswerMessage(answer='success')
            self.__is_handling=False
        else:
            error_info=self.__UserLogger.getErrorDescription()
            answer_msg=self.__AccessAnswerMessage(answer='error', error_info=error_info)

        client.sendwh(answer_msg.to_string())"""
        
