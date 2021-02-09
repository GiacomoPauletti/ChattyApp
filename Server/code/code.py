import abc
import threading

class ChatID:
    def __init__(self, value : str):
        self.value=value

    ...


class Chat(abc.ABC):
    def __init__(self, chatid : ChatID):
        self.chatid=chatid

    ...



#!! devo stare attento ad usare composition over inheritance
class User:      #observer pattern between Chat and Client
    def __init__(self):
        pass

    def send(self, message):
        ...


class UserHandler:
    def __init__(self, user : User):
        User : self.user = user

    def loop(self):
        loopThread=threading.Thread(target=self.__loop)

    def __loop(self):
        """
            self.user.send(message)
        """
        ...

class UserFactory(abc.ABC):
    @abc.abstractmethod
    def createUser(self) -> User:
        pass

class BasicUserFactory(UserFactory):
    def createUser(self) -> User:
        return User()



class Message:
    def __init__(self, header : str, content : str):
        self.__header = header
        self.__content = content

    def getHeader(self):
        return self.__header
    
    def getContent(self):
        return self.__content


"""

"""