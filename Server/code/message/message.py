import abc
from utilities.chatid import Chatid


class ChatMessage:

    @classmethod
    def from_string(cls, message : str):
        """Create a ChatMessage class from a string of the form: sender_private_name|receiver_chat|content"""

        if message.count('|') != 2:
            print('WARNING: the string passed had not the right number of fields (2)')
            return None

        sender_private_name, receiver_chat_id, content = message.split('|')
        receiver_chat_id=Chatid.from_string(receiver_chat_id)

        return cls(sender=sender_private_name, chat=receiver_chat_id, content=content)

    def __init__(self, sender : str, chat: Chatid,  content : str):
        self.__sender_private_name=sender
        self.__receiver_chat_id=chat
        self.__content = content

    def get_sender(self):
        return self.__sender_private_name

    def get_chat(self):
        return self.__receiver_chat_id

    def get_content(self):
        return self.__content

    def __str__(self):
        return f'{self.__sender_private_name}|{self.__receiver_chat_id.get_value()}|{self.__content}'

class NotificationMessage:  #per ora è tale e quale al ChatMessage, in futuro va cambiato

    @classmethod
    def from_string(cls, message : str):
        """Create a NotificationMessage class from a string of the form: sender_private_name|receiver_chat|content"""

        if message.count('|') != 2:
            print('WARNING: the string passed had not the right number of fields (2)')
            return None

        sender_private_name, receiver_chat_id, content = message.split('|')
        receiver_chat_id=Chatid.from_string(receiver_chat_id)

        return cls(sender=sender_private_name, chat=receiver_chat_id, content=content)

    def __init__(self, sender : str, chat: Chatid,  content : str):
        self.__sender_private_name=sender
        self.__receiver_chat_id=chat
        self.__content = content

    def get_sender(self):
        return self.__sender_private_name

    def get_chat(self):
        return self.__receiver_chat_id

    def get_content(self):
        return self.__content

    def __str__(self):
        return f'{self.__sender_private_name}|{self.__receiver_chat_id}|{self.__content}'

class AccessAnswerMessage:

    @classmethod
    def from_string(cls, message : str):

        if message.count('|') != 1:
            print('WARNING: the string passed had not the right number of fields (1)')
            return None

        answer, error = message.split('|')

        return cls(answer=answer, error=error)

    def __init__(self, answer, error=''):
        self.__answer=answer
        self.__error=error

    def get_answer(self):
        return self.__answer

    def get_error(self):
        return self.__error

    def __str__(self):
        return f'{self.__answer}|{str(self.__error)}'
