class List:
    """
    Iterator with size attribute
    """
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == self.size:
            raise StopIteration
        self.index += 1
        return self.data[self.index]
