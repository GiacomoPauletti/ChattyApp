import abc
import threading
import socket

from message.abcs import Message
from chat.chat import Chat
from user.user import User
from user.user_listeners import UnaccessedUserListener, AccessedUserListener
from handlers.access_handler import AccessHandler
from storage.abcs import UserLogger, UserRegister
from utilities.registers import AuthorizedUserRegister

global_user_logger=UserLogger()
global_user_register=UserRegister()

auth_users=AuthorizedUserRegister()
accesshandler=AccessHandler(global_user_logger, global_user_register, Message, Message, auth_users)


if __name__ == "__main__":
    ...

