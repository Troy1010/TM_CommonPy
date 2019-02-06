import tkinter as tk
from .Cell_Inheritable import Cell_Inheritable
import rx


class Label_DirectStream(Cell_Inheritable, tk.Label):

    def __init__(self, *args, display=None, **kwargs):
        super().__init__(*args, **kwargs)
        # make FocusOut an observable
        self.FocusOut_stream = rx.subjects.Subject()
        self.bind("<FocusOut>", lambda event: self.FocusOut_stream.on_next(None), add="+")
        #
        if display is None:
            self.DisplayHandler = lambda x: x
        else:
            self.DisplayHandler = display
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
            self.stream = value
            self.DisposeDisposables()
            # when stream changes, change my text

            def AssignText(value):
                self.text = value
            self.cDisposables.append(self.stream.subscribe(AssignText))
            # when my text changes, change stream

            def OnFocusOut(nothing):
                value = self.ValidationHandler(self.text) if self.ValidationHandler is not None else self.text
                self.stream.on_next(value)
            self.cDisposables.append(self.FocusOut_stream.subscribe(OnFocusOut))
            #
            return
        #
        if self.ValidationHandler is not None:
            value = self.ValidationHandler(value)
        value = self.DisplayHandler(value)
        self.configure(text=value)
        # state = self["state"]
        # self.configure(state='normal')
        # self.delete(0, tk.END)
        # if self.ValidationHandler is not None:
        #     value = self.ValidationHandler(value)
        # value = self.DisplayHandler(value)
        # if value is not None:
        #     self.insert(0, value)
        # self.configure(state=state)

    def select_text(self):
        self.select_range(0, 'end')
        self.icursor('end')

    def FocusNothing(self):
        self.winfo_toplevel().focus_set()
