
class AccessError:
    def __init__(self, field, description=''):
        self.__field=field
        self.__description=description

    def get_field(self):
        return self.__field

    def get_description(self):
        return self.__description

    def __str__(self):
        return f'AccessError|{self.__field}'
