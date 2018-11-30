import openpyxl

#len() will return 1 if either 0 or 1 col exists.
def GetMaxCol(vSheet):
    if IsEmptySheet(vSheet):
        return 0
    return len(vSheet['1'])

def IsEmptySheet(vSheet):
    for cRows in vSheet.iter_rows():
        for vCell in cRows:
            if not vCell.value is None:
                return False
    return True

def PosByCell(vCell,iColAdjustment=0,iRowAdjustment=0):
    return openpyxl.utils.get_column_letter(openpyxl.utils.column_index_from_string(vCell.column)+iColAdjustment)+str(vCell.row+iRowAdjustment)

def PosByXY(x,y):
    return openpyxl.utils.get_column_letter(x+1)+str(y+1)
