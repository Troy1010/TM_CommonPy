import tkinter as tk


class Entry(tk.Entry):
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

    @property
    def text(self):
        return self.get()

    @text.setter
    def text(self, value):
        state = self["state"]
        self.configure(state='normal')
        self.delete(0, tk.END)
        if value is not None:
            if self.ValidationHandler is not None:
                value = self.ValidationHandler(value)
            self.insert(0, value)
        self.configure(state=state)

    def select_text(self):
        self.select_range(0, 'end')
        self.icursor('end')
