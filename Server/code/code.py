import abc
import threading
from typing import List

class IObserver(abc.ABC):
    @abc.abstractmethod
    def update(self):
        ...

class IObservable(abc.ABC):
    @abc.abstractmethod
    def registerObserver(self, observer : IObserver) -> None:
        ...

    def removeObserver(self, observer : IObserver) -> None:
        ...

    def notifyObservers(self) -> None:
        ...


class ChatID:
    def __init__(self, value : str):
        self.value=value

    ...


class Chat(IObservable):
    def __init__(self, chatid : ChatID):
        self.chatid=chatid
        self.___observers=[]

    def registerObserver(self, observer: IObserver) -> None:
        self.___observers.append(observer)

    def removeObserver(self, observer : IObserver) -> None:
        if observer not in self.___observers:
            return None
        self.___observers.remove(observer)

    def notify(self):
        for observer in self.__observers:
            observer.update()

    



#!! devo stare attento ad usare composition over inheritance
class User(IObservable):      #observer pattern between Chat and Client
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



class Message:
    @classmethod
    def fromString(cls, string : str):
        closing_header_index=string.index('>')
        header=string[1:closing_header_index]
        content=string[closing_header_index+1:]

        return cls(header=header, content=content)

    @classmethod
    def fromTuple(cls, tpl : tuple):
        if len(tpl) != 2:
            return None
        return cls(header=tpl[0], content=tpl[1])

    @classmethod
    def fromDict(cls, dictionary : dict):
        return cls(header=dictionary['header'], content=dictionary['content'])

    def __init__(self, header : str, content : str):
        self.__header = header
        self.__content = content

    def getHeader(self):
        return self.__header
    
    def getContent(self):
        return self.__content

    def __str__(self):
        return f'<{self.__header}>{self.__content}'
