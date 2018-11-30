
class Counter:
    def __init__(self):
        self.iCount = 0

    def __call__(self):
        self.iCount += 1
        return self.iCount - 1

    def reset(self):
        self.__init__()
