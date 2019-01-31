class Cell_Inheritable():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cDisposables = []
        self.ValidationHandler = None

    def MakeValid(self):
        """ Useful if text is changed outside of its setter """
        self.text = self.text

    def AddDisposable(self, disposable):
        self.cDisposables.append(disposable)

    def destroy(self):
        for disposable in self.cDisposables:
            disposable.dispose()
        super().destroy()

    @property
    def column(self):
        return self.grid_info()['column']

    @property
    def row(self):
        return self.grid_info()['row']
