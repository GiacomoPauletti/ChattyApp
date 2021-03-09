import abc

class HandlerFactorY(abc.ABC):
    @abc.abstracmethod
    def get_handler(self):
        ...
