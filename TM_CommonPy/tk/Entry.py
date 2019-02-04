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
        if isinstance(value, rx.Observable):
            self.DisposeDisposables()
            # when stream changes, change entry text

            def AssignText(value):
                self.text = value
            self.cDisposables.append(value.subscribe(AssignText))
            # when entry text changes, change stream

            def OnFocusOut_FeedToStream(event):
                if not hasattr(self, '__temp_obs'):
                    self.__temp_obs = rx.subjects.Subject()
                    self.cDisposables.append(self.__temp_obs.distinct_until_changed().subscribe(value))
                if self.ValidationHandler:
                    self.__temp_obs.on_next(self.ValidationHandler(self.get()))
                else:
                    self.__temp_obs.on_next(self.get())
            self.bind("<FocusOut>", OnFocusOut_FeedToStream, add="+")
            self.bind("<FocusOut>", lambda event: print("focus out"), add="+")
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

    def FocusNothing(self):
        self.winfo_toplevel().focus_set()
