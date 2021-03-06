from abcs.py import UserLogger, UserRegister

class UserAccesserFactory:
    def __init__(self, user_logger : UserLogger, user_register : UserRegister):
        self.__user_logger=user_logger
        self.__user_register=user_register
    
    def get_user_logger(self):
        return self.__user_logger

    def get_user_register(self):
        return self.__user_register

class UserTextLogger(UserLogger):
    def __init__(self,...):
        pass

class UserTextRegister(UserRegister):
    def __init__(self, ...):
        pass
