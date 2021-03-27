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

