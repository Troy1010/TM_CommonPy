import tkinter as tk
from .Cell_Inheritable import Cell_Inheritable
from .DirectStream_Inheritable import DirectStream_Inheritable
import rx
import TM_CommonPy as TM  # noqa


class Entry_DirectStream(DirectStream_Inheritable, Cell_Inheritable, tk.Entry):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # trigger text setter
        if 'stream' not in kwargs and 'text' in kwargs:
            self.text = kwargs['text']

    @property
    def text(self):
        return self.get()

    @text.setter
    def text(self, value):
        assert(not isinstance(value, rx.Observable))
        if self.ValidationHandler is not None:
            value = self.ValidationHandler(value)
        if self.DisplayHandler is not None:
            value = self.DisplayHandler(value)
        state = self["state"]
        self.configure(state='normal')
        self.delete(0, tk.END)
        if value is not None:
            self.insert(0, value)
        self.configure(state=state)

    def select_text(self):
        self.select_range(0, 'end')
        self.icursor('end')


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
        if isinstance(value, rx.Observable):
            self.DisposeDisposables()
            # when stream changes, change entry text

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
