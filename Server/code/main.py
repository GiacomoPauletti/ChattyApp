import abc
import threading
import socket

from chat.chat import Chat
from user.user import User, get_text_user_initializator
from user.user_servers import UnauthUserServer, AuthUserServer
from handlers.access_handler import text_access_handler_factory
#from handlers.notification_handler import text_notification_handler_factory
from handlers.chat_handler import text_chat_handler_factory, ChatHandlerServer
from storage.chat_storage import TextUserChatStorage
import utilities.registers as rgs

#registers initialization
auth_user_register=rgs.AuthorizedUserRegister()
active_user_register=rgs.ActiveUserRegister()
active_chat_register=rgs.ActiveChatRegister(active_user_register, TextUserChatStorage(), Chat)

#handlers initialization
access_handler=text_access_handler_factory(authorized_user_register=auth_user_register)
chat_handler=text_chat_handler_factory(active_user_register, active_chat_register)

#servers initialization
unauth_user_server=UnauthUserServer(access_handler)

user_initializator=get_text_user_initializator(active_user_register, active_chat_register)
auth_user_Server=AuthUserServer(auth_user_register, user_initializator)

chat_handler_server=ChatHandlerServer(chat_handler)


if __name__ == "__main__":

    #servers listening
    unauth_user_server.listen()
    auth_user_server.listen()
    chat_handler_server.listen()
    
    is_online=True
    while is_online:
        print("[MAIN] server is now online")
        break
    
