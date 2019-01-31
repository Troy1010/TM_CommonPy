import tkinter as tk
from .Cell_Inheritable import Cell_Inheritable
import rx


class Entry(Cell_Inheritable, tk.Entry):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # trigger text setter
        if 'text' in kwargs:
            self.text = kwargs['text']

    @property
    def text(self):
        return self.get()

    @text.setter
    def text(self, value):
        # text
        if isinstance(value, rx.subjects.BehaviorSubject):
            def AssignText(value):
                self.text = value
            self.cDisposables.append(value.subscribe(AssignText))
            return
        #
        state = self["state"]
        self.configure(state='normal')
        self.delete(0, tk.END)
        if self.ValidationHandler is not None:
            value = self.ValidationHandler(value)
        if value is not None:
            self.insert(0, value)
        self.configure(state=state)

    def select_text(self):
        self.select_range(0, 'end')
        self.icursor('end')
