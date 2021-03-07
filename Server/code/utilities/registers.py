class AuthorizedUserRegister:

    def __init__(self, maximum=None):
        self.__auth_user_dict=[]

    def add(self, user_address, user_private_name):
        if maximum and len(self.__auth_user_dict) < maximum:
            self.__auth_user_dict[user_address] = user_private_name

    def remove(self, user_address):
        self.__auth_user_dict.pop(user_address, None)

    def is_authorized_address(self, user_address):
        return bool(self.__auth_user_dict.get(user_address, False))

    def is_authorized_name(self, user_private_name):
        return user_private_name in self.__auth_user_dict.values()

    def get_name_by_address(self, user_address):
        return self.__auth_user_dict.get(user_address, None)

"""
class ActiveUserList:
    def __init__(self):
        self.__active_users={}
    
    def add_user(self, user : User, address : str):
        self.__active_users[address]=user

    def remove_user_by_address(self, address):
        self.__active_users.pop(address, False)

    def is_address_active(self, address : str):
        return address in self.__active_users.keys()
    
    def is_user_active(self, user : User):
        return user in self.__active_users.values()
        
    def find_user_by_address(self, address : str):
        return self.__active_users.get(address, None)

    def find_address_by_user(self, user : User):
        for (current_address, current_user) in self.__active_users:
            if current_user == user:
                return current_address
"""

