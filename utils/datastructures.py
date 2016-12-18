class List(list):
    """
    list with size attribute
    """
    @property
    def size(self):
        return self.__len__()
