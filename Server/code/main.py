import abc
import threading
from typing import List
import socket

from message import Message
from chat import Chat
from user import User

class UserListener:
    def listen(self):
        with socket.create_server(('', 8000)):
            conn, addr = socket.accept()    #timeout=...

            #create new User
            #make the UserActivityHandler (or whatever is the one which login or register the user) listen for the new user
    




