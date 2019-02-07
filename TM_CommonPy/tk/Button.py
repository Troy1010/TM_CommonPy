import tkinter as tk
from .Cell_Inheritable import Cell_Inheritable
from .DirectStream_Inheritable import DirectStream_Inheritable
import rx


class Button(DirectStream_Inheritable, Cell_Inheritable, tk.Button):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # trigger text setter
        if 'stream' not in kwargs and 'text' in kwargs:
            self.text = kwargs['text']

    @property
    def text(self):
        return self['text']

    @text.setter
    def text(self, value):
        assert(not isinstance(value, rx.Observable))
        if self.ValidationHandler is not None:
            value = self.ValidationHandler(value)
        if self.DisplayHandler is not None:
            value = self.DisplayHandler(value)
        self.configure(text=value)
