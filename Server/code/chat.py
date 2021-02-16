from utilities.abcs import *

class Chatid
    def __init__(self, value : str):
        self.value=value

    ...


class Chat(IObservable):
    def __init__(self, chatid : Chatid):
        self.chatid=chatid
        self.__users=[]

    def register_user(self, user: IObserver) -> None:
        self.__users.append(observer)

    def removeObserver(self, user : IObserver) -> None:
        if observer not in self.___observers:
            return None
        self.__users.remove(user)

    def notify(self):
        for user in self.__users:
            users.update()
