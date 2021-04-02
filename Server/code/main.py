import abc
import threading
import socket

from message.message import AccessMessage, AccessAnswerMessage
from chat.chat import Chat
from user.user import User, get_text_user_initializator
from user.user_listeners import UnauthUserListener, AuthUserListener
from handlers.access_handler import text_access_handler_factory
from utilities.registers import AuthorizedUserRegister

auth_users=AuthorizedUserRegister()

access_handler=text_access_handler_factory(user_message=AccessMessage, access_answer_message=AccessAnswerMessage, authorized_user_register=auth_users)

unauth_user_listener=UnauthUserListener(access_handler)
auth_user_listener=AuthUserListener(auth_users, get_text_user_initializator())

if __name__ == "__main__":

    unauth_user_listener.listen()
    auth_user_listener.listen()
    
    is_online=True
    while is_online:
        print("[MAIN] server is now online")
        break
    
