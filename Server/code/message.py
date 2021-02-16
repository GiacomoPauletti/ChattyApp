import abc

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
        return f'{self.__header}|{self.__content}'


class IMessageFactory(abc.ABC):
    @abc.abstractmethod
    def createMessage(self):
        return Message()

class FromStringMessageFactory(IMessageFactory):
    def createMessage(self, string : str):
        return Message._fromString(string)

class FromTupleMessageFactory(IMessageFactory):
    def createMessage(self, tpl : tuple):
        return Message._fromTuple(tpl)

class FromDictMessageFactory(IMessageFactory):
    def createMessage(self, dictionary : dict):
        return Message._fromDict(dictionary)
