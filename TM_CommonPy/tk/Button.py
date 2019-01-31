import tkinter as tk
from .Cell_Inheritable import Cell_Inheritable
import rx


class Button(Cell_Inheritable, tk.Button):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # trigger text setter
        if 'text' in kwargs:
            self.text = kwargs['text']

    @property
    def text(self):
        return self['text']

    @text.setter
    def text(self, value):
        # text
        if isinstance(value, rx.subjects.BehaviorSubject):
            def AssignText(value):
                self.text = value
            self.cDisposables.append(value.subscribe(AssignText))
            return
        #
        if self.ValidationHandler is not None:
            value = self.ValidationHandler(value)
        self.configure(text=value)
