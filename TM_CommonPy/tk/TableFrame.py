import tkinter as tk
import TM_CommonPy as TM
from . import Constants
from TM_CommonPy._Logger import TMLog


class TableFrame(tk.Frame):
    def Hello():
        TMLog.debug("Hello")

    def GetCell(self, row, column):
        return self.grid_slaves(row, column)[0]

    def FocusNextWritableCell(self, cellToSearchFrom=None, searchDirection=Constants.HORIZONAL):
        TMLog.debug("FocusNextWritableCell`Open")
        if searchDirection == Constants.HORIZONAL:
            TMLog.debug("horiz")
        else:
            TMLog.debug("vert")
