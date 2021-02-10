"""import sys
sys.path.append("utilities")"""

from utilities.abcs import IObservable, IObserver
import abc
import threading

#!! devo stare attento ad usare composition over inheritance
class User(IObserver):      #observer pattern between Chat and Client
    def __init__(self):
        pass

    def update(self):
        ...

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
