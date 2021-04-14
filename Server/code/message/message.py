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

class ChatRequestMessage:

    @classmethod
    def from_string(cls, message : str):
        """Create a ChatRequestMessage class from a string of the form: action|chatid"""

        if message.count('|') != 2:
            print('WARNING: the string passed had not the right number of fields (3)')
            return None

        action, users, chatid = message.split('|')
        users=users.split(';')
        return cls(action=action, users=users, chatid=chatid)

    def __init__(self, action, users, chatid):
        self.__action=action
        self.__users=users
        self.__chatid=chatid

    def get_action(self):
        return self.__action

    def get_users(self):
        for user in self.__users:
            yield user
    
    def get_users_str(self):
        return ';'.join(self.__users)

    def get_chat(self):
        return self.__chatid

    def __str__(self):
        return f'{self.__action}|{";".join(self.__users)}|{self.__chatid}'

class ChatAnswerMessage:

    @classmethod
    def from_string(cls, message : str):
        """Create a ChatAnswerMessage class from a string of the form: answer|content"""

        if message.count('|') != 1:
            print('WARNING: the string passed had not the right number of fields (2)')
            return None

        answer, content = message.split('|')

        return cls(answer=answer, content=content)

    def __init__(self, answer, content):
        self.__answer=answer
        self.__content=content

    def get_answer(self):
        return self.__answer

    def get_content(self):
        return self.__content

    def __str__(self):
        return f'{self.__answer}|{self.__content}'

        self.__content=content
    

class NotificationMessage:  

    @classmethod
    def from_string(cls, message : str):
        """Create a NotificationMessage class from a string of the form: sender_private_name|users|content"""

        if message.count('|') != 2:
            print('WARNING: the string passed had not the right number of fields (3)')
            return None

        sender_private_name, users, content = message.split('|')

        return cls(sender=sender_private_name, users=users, content=content)

    def __init__(self, sender : str, users : str,  content : str):
        self.__sender_private_name=sender
        self.__users=users
        self.__content = content

    def get_sender(self):
        return self.__sender_private_name

    def get_users(self):
        for user in self.__users.split(';'):
            yield user

    def get_content(self):
        return self.__content

    def __str__(self):
        return f'{self.__sender_private_name}|{self.__users}|{self.__content}'

class NotificationRequestMessage:

    @classmethod
    def from_string(cls, message : str):

        if message.count('|') != 1:
            print('WARNING: the string passed had not the right number of fields (1)')
            return None

        action, sender_private_name= message.split('|')

        return cls(action=action, sender=sender_private_name)

    def __init__(self, action : str, sender : str):
        self.__action=action
        self.__sender=sender

    def get_action(self):
        return self.__action
    
    def get_sender(self):
        return self.__sender

    def __str__(self):
        return f'{self.__action}|{self.__sender}'

class NotificationAnswerMessage:

    @classmethod
    def from_string(cls, message : str):

        if message.count('|') != 1:
            print('WARNING: the string passed had not the right number of fields (1)')
            return None

        answer, content= message.split('|')

        return cls(answer=answer, content=content)

    def __init__(self, answer, content):
        self.__answer=answer
        self.__content=content

    def get_answer(self):
        return self.__answer
    
    def get_content(self):
        return self.__content

    def __str__(self):
        return f'{self.__answer}|{self.__content}'
    

class AccessMessage:

    @classmethod
    def from_string(cls, message : str):

        if message.count('|') != 3:
            print('WARNING: the string passed had not the right number of fields (1)')
            return None

        action, private_name, password, email= message.split('|')

        return cls(action=action, private_name=private_name, password=password, email=email)

    def __init__(self, action, private_name, password, email):
        self.__action=action
        self.__private_name=private_name
        self.__password=password
        self.__email=email

    def get_action(self):
        return self.__action

    def get_private_name(self):
        return self.__private_name

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def __str__(self):
        return f'{self.__action}|{self.__private_name}|{self.__password}|{self.__email}'

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
