import tkinter as tk
from . import Constants


class TableFrame(tk.Frame):
    def GetCell(self, row, column):
        try:
            return self.grid_slaves(row, column)[0]
        except IndexError:
            return None

    def ClearTable(self):
        for child in self.winfo_children():
            child.grid_forget()
            child.destroy()

    def ClearRow(self, row):
        for child in self.grid_slaves(row):
            child.grid_forget()
            child.destroy()

    def GetMaxColumn(self):
        return self.grid_size()[0] - 1

    def GetMaxRow(self):
        return self.grid_size()[1] - 1

    def InsertRow(self, row):
        for w in self.winfo_children():
            if 'row' not in w.grid_info():
                continue
            if row <= w.grid_info()['row']:
                w.grid_configure(row=w.grid_info()['row']+1)

    def IsRowEmpty(self, row):
        try:
            return self.grid_slaves(row)[0] is None
        except IndexError:
            return True

    def FocusNothing(self):
        self.winfo_toplevel().focus_set()

    def FocusNextWritableCell(self, cellToSearchFrom=None, searchDirection=Constants.HORIZONAL):
        # Determine firstRow, firstCol
        if cellToSearchFrom:
            firstRow = cellToSearchFrom.row
            firstCol = cellToSearchFrom.column
        else:
            firstRow = 0
            firstCol = 0
        # Determine curCol, curRow
        if searchDirection == Constants.HORIZONAL:
            curCol = firstCol + 1
            curRow = firstRow
        else:
            curCol = firstCol
            curRow = firstRow + 1

        # Search
        iMaxColumn = self.GetMaxColumn()
        iMaxRow = self.GetMaxRow()
        while not (curCol == firstCol and curRow == firstRow):
            cell = self.GetCell(curRow, curCol)
            # Is this cell writable
            if cell and "entry" in str(type(cell)).lower() and cell.cget('state') == tk.NORMAL:
                cell.focus_set()
                return
            #
            if searchDirection == Constants.HORIZONAL:
                if curCol < iMaxColumn:
                    curCol += 1
                elif curRow < iMaxRow:
                    curCol = 0
                    curRow += 1
                else:
                    curCol = 0
                    curRow = 0
            else:
                if curRow < iMaxRow:
                    curRow += 1
                elif curCol < iMaxColumn:
                    curCol += 1
                    curRow = 0
                else:
                    curCol = 0
                    curRow = 0
        # Focus nothing
        self.winfo_toplevel().focus_set()
