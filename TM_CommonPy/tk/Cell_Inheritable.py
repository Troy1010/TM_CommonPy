

class Cell_Inheritable():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cDisposables = []
        self._ValidationHandler = None

    def MakeValid(self):
        """ Useful if text is changed outside of its setter """
        self.text = self.text

    def AddDisposable(self, disposable):
        self.cDisposables.append(disposable)

    def DisposeDisposables(self):
        for disposable in self.cDisposables:
            disposable.dispose()
        self.cDisposables.clear()

    def destroy(self):
        self.DisposeDisposables()
        super().destroy()

    @property
    def ValidationHandler(self):
        return self._ValidationHandler

    @ValidationHandler.setter
    def ValidationHandler(self, value):
        self._ValidationHandler = value
        self.MakeValid()

    @property
    def column(self):
        return self.grid_info()['column']

    @property
    def row(self):
        return self.grid_info()['row']
