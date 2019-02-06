import tkinter as tk
from .Cell_Inheritable import Cell_Inheritable
import rx
import TM_CommonPy as TM  # noqa


class Entry_DirectStream(Cell_Inheritable, tk.Entry):

    def __init__(self, *args, display=None, stream=None, **kwargs):
        super().__init__(*args, **kwargs)
        # make FocusOut an observable
        self.FocusOut_stream = rx.subjects.Subject()
        self.bind("<FocusOut>", lambda event: self.FocusOut_stream.on_next(None), add="+")
        #
        assert(callable(display) or display is None)
        self.DisplayHandler = display
        # trigger stream setter
        if stream:
            self.stream = stream
        # trigger text setter
        if not stream and 'text' in kwargs:
            self.text = kwargs['text']

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, stream):
        assert(isinstance(stream, rx.Observable))
        self._stream = stream
        self.DisposeDisposables()
        # when stream changes, change my text

        def AssignText(value):
            self.text = value
        self.cDisposables.append(self._stream.subscribe(AssignText))
        # when my text changes, change stream

        def OnFocusOut(nothing):
            value = self.ValidationHandler(self.text) if self.ValidationHandler is not None else self.text
            self._stream.on_next(value)
        self.cDisposables.append(self.FocusOut_stream.subscribe(OnFocusOut))

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

    def FocusNothing(self):
        self.winfo_toplevel().focus_set()


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

    def FocusNothing(self):
        self.winfo_toplevel().focus_set()
