from collections import UserList, UserDict


class NSDict(UserDict):
    """
    A dict with namespace features
    """
    def __init__(self, data):
        self.data = data
        for k, v in data.items():
            if '.' in k:
                namespace, key = k.split('.')
                nsdata = getattr(self, namespace, {})
                nsdata[key] = v
                setattr(self, namespace, nsdata)


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
