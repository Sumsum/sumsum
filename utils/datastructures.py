from collections import UserList


class List(UserList):
    """
    list with some exta (ruby) properties
    """
    def __init__(self, data=None):
        self.data = data or []

    @property
    def size(self):
        return self.__len__()

    @property
    def first(self):
        try:
            return self.data[0]
        except IndexError:
            return None
