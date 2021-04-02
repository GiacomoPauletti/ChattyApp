class AuthorizedUserRegister:

    def __init__(self, maximum=None):
        self.__auth_dict=[]
        self.__maximum=maximum

    def add(self, address, private_name):
        if self.__maximum and len(self.__auth_dict) < self.__maximum:
            self.__auth_dict[address] = private_name

    def remove(self, address):
        self.__auth_dict.pop(address, None)

    def is_authorized_address(self, address):
        return bool(self.__auth_dict.get(address, False))

    def is_authorized_name(self, private_name):
        return private_name in self.__auth_dict.values()

    def get_name_by_address(self, address):
        return self.__auth_dict.get(address, None)



        


class ActiveUserRegister:

    def __init__(self):
        self.__active_users={}

    def add(self, private_name, server_user):
        if not private_name in self.__active_users.keys():
            self.__active_users[private_name]=server_user
            return True
        return False

    def get(self, private_name):
        return self.__active_users.get(private_name, None)

    def remove(self, private_name):
        return bool(self.__active_users.pop(private_name, False))
    
    def pop(self, private_name):
        return self.__active_users.pop(private_name, None)


class ActiveChatRegister:

    def __init__(self, active_user_register, user_chat_storage, chat_class):
        self.__active_chats={}
        self.__active_user_register=active_user_register

        self.__user_chat_storage=user_chat_storage
        self.__Chat=chat_class

    def add(self, chatid, chat_obj):
        if not chatid in self.__active_chats.keys():
            self.__active_chats[chatid]=chat_obj
            return True
        return False

    def get(self, chatid, force=False):
        
        is_active=chatid in self.__active_chats.keys() 
        if not is_active and force:
            chat_obj=self._activate_chat(chatid)
            self.__active_chats[chatid]=chat_obj


        return self.__active_chats.get(chatid, None)

    def remove(self, chatid):
        return bool(self.__active_chats.pop(chatid, False))
    
    def pop(self, chatid):
        return self.__active_chats.pop(chatid, None)

    def _activate_chat(self, chatid):
        chat_obj=self.__Chat(chatid)

        for private_name in self.__user_chat_storage.get_users(chatid):
            user_obj=self.__active_user_register.get(private_name)
            if user_obj:
                chat_obj.register_user(user_obj)

        return chat_obj


"""
class ActiveUserList:
    def __init__(self):
        self.__active_users={}
    
    def add_user(self, user : User, address : str):
        self.__active_users[address]=user

    def remove_by_address(self, address):
        self.__active_users.pop(address, False)

    def is_address_active(self, address : str):
        return address in self.__active_users.keys()
    
    def is_active(self, user : User):
        return user in self.__active_users.values()
        
    def find_by_address(self, address : str):
        return self.__active_users.get(address, None)

    def find_address_by_user(self, user : User):
        for (current_address, current_user) in self.__active_users:
            if current_user == user:
                return current_address
"""

