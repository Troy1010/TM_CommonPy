import rx
import TM_CommonPy as TM  # noqa


class DirectStream_Inheritable():

    def __init__(self, *args, display=None, stream=None, **kwargs):
        super().__init__(*args, **kwargs)
        assert(callable(display) or display is None)
        self.DisplayHandler = display
        # make FocusOut an observable
        self.FocusOut_stream = rx.subjects.Subject()
        self.bind("<FocusOut>", lambda event: self.FocusOut_stream.on_next(None), add="+")
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
