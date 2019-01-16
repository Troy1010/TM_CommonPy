import tkinter as tk
from . import Constants
from TM_CommonPy._Logger import TMLog


class TableFrame(tk.Frame):
    def GetCell(self, row, column):
        try:
            return self.grid_slaves(row, column)[0]
        except IndexError:
            return None

    def FocusNextWritableCell(self, cellToSearchFrom=None, searchDirection=Constants.HORIZONAL):
        if cellToSearchFrom:
            firstRow = cellToSearchFrom.row
            firstCol = cellToSearchFrom.column
        else:
            firstRow = cellToSearchFrom.row
            firstCol = cellToSearchFrom.column
        if searchDirection == Constants.HORIZONAL:
            curCol = firstCol + 1
            curRow = firstRow
        else:
            curCol = firstCol
            curRow = firstRow + 1

        while not (curCol == firstCol and curRow == firstRow):
            cell = self.GetCell(curRow, curCol)
            if "entry" in str(type(cell)).lower() and cell.cget('state') == tk.NORMAL:
                cell.focus_set()
                return
            if searchDirection == Constants.HORIZONAL:
                if self.GetCell(curRow, curCol + 1):
                    curCol += 1
                elif self.GetCell(curRow + 1, 0):
                    curCol = 0
                    curRow += 1
                elif self.GetCell(0, 0):
                    curCol = 0
                    curRow = 0
                else:
                    break
            else:
                if self.GetCell(curRow + 1, curCol):
                    curRow += 1
                elif self.GetCell(0, curCol + 1):
                    curCol += 1
                    curRow = 0
                elif self.GetCell(0, 0):
                    curCol = 0
                    curRow = 0
                else:
                    break
        self.winfo_toplevel().focus_set()
