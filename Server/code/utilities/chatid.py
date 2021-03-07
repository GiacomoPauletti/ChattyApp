class Chatid: 
     
    @classmethod 
    def from_string(cls, string : str): 
        return cls(value=string) 
 
    def __init__(self, value : str): 
        self.__value=value 
 
    def getValue(self): 
        return self.__value

