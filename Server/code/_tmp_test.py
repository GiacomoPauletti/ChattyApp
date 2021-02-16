import abc

class IObservable(abc.ABC):
    ...

class IObserver(abc.ABC):
    ...

class IRemoteProxy(abc.ABC):
    ...

class Message:
    def __init__(self, header, content):
        self.__header=header
        self.__content=content

    def getHeader(self):
        return self.__header

    def getContent(self):
        return self.__content


class ClientHandler(self):
    def __init__(self, user):
        self.__user=user

    def handler(self):
        while True:
            try:
                message=self.__user.receive(100)
            except:
                continue

            header, content = message.split('|')
            msg_object=Message(header=header, content=content)



class ChatHandler(IObservable):
    def __init__(self, chatid):
        self.__id=chatid
        self.__users=users
        self.__active_users=None

    def register_user(self, user : User) -> None:
        self.__users.append[user]

    def remove_user(self, user : User):
        if user in self.__users:
            self.__users.remove(user)

    def notify_users(self, message):
        #sends the new message to everyone who joined the chat
        for user in self.__users:
            user.receive_message(message)
        pass
    
    def register_active_user(self, user : User) -> None:
        if user not in self.__active_users:
            self.__active_users.append(user)

    def remove_active_user(self, user : User) -> None:
        if user in self.__active_users:
            self.__active_users.remove(user)
    
    def listen_active_users(self):
        for active_user in self.__active_users:
            #aspetta per un certo tempo un messaggio dall'utente
            
            try:
                #message=active_user.receive(waitfor=2)
                #self.notify_users(message)
                pass
            except:
                continue
            
class ProfileHandler:
    """ serve per ricevere i messaggi dei cambiamenti del profilo"""
    def __init__(self, users):
        self.__users=users
    
    def listen_users(self):
        for user in self.__users:
            #message=user.receive(waitfor=20)=
            #new_picture=message.split('|')[1]
            #notification_message=Message(header='newfriendpic', content=f'friend={user.get_id()}', picture=f'{new_picture}')
            for friend in user.get_friends():
                

class UserActivityHandler:
    """ serve per riceve i messaggi di login e di logout"""
    pass

class Profile:
    def __init__(self, picture, biography, state):
        self.picture=picture
        self.biography=biography
        self.state=state
"""
class User(IRemoteProxy, IObserver):
    def __init__(self, userid, profile):
        self.__id=userid
        self.__profile=profile
        self.__current_chat=None
        self.__client_handler=None
        self.__friends=None

    def receive_message(self, message : Message):
        ...

    def send_message(self, message : Message):
        ...

    def change_profile_picture(self, new_picture):
        self.__profile.picture=new_picture

    def change_profile_biography(self, new_biography : str):
        self.__profile.biography=new_biography

    def change_profile_state(self, new_state : str):
        self.__profile.state=new_state
"""
class Register:
    def __init__(self, ...):
        pass

    def get_user_by_id(self, userid):
        #do some stuff and then
        #return user

    def register_user(self, user):
        pass

    def login_user(self, user):
        pass

    def logout_user(self, user):
        pass

class UserFactory(abc.ABC)
    @abc.abstractmethod
    def createUser(self, userid):
        ...
