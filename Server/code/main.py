import abc
import threading
import socket

from message.message import AccessMessage, AccessAnswerMessage
from chat.chat import Chat
from user.user import User, get_text_user_initializator
from user.user_listeners import UnauthUserListener, AuthUserListener
from handlers.access_handler import text_access_handler_factory
from storage.chat_storage import TextUserChatStorage
import utilities.registers as rgs

auth_user_register=rgs.AuthorizedUserRegister()
active_user_register=rgs.ActiveUserRegister()
active_chat_register=rgs.ActiveChatRegister(active_user_register, TextUserChatStorage(), Chat)


access_handler=text_access_handler_factory(user_message_class=AccessMessage, answer_message_class=AccessAnswerMessage, authorized_user_register=auth_user_register)

unauth_user_listener=UnauthUserListener(access_handler)
auth_user_listener=AuthUserListener(auth_user_register, get_text_user_initializator(active_chat_register))

if __name__ == "__main__":

    unauth_user_listener.listen()
    auth_user_listener.listen()
    
    is_online=True
    while is_online:
        print("[MAIN] server is now online")
        break
    
