from utilities.abcs import *

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
