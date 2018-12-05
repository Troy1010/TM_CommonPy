import TM_CommonPy as TM
import os


class WorkspaceContext:
    def __init__(self, sPath, sSource=None, bPostDelete=False, bCDInto=True, bPreDelete=False):
        self.bCDInto = bCDInto
        self.bPostDelete = bPostDelete
        self.sPath = sPath
        self.sSource = sSource
        self.bPreDelete = bPreDelete

    def __enter__(self):
        if self.bPreDelete:
            TM.Delete(self.sPath)
        if self.sSource is None:
            TM.TryMkdir(self.sPath)
        else:
            TM.Copy(self.sSource, self.sPath)
        if self.bCDInto:
            self.OldCWD = os.getcwd()
            os.chdir(self.sPath)

    def __exit__(self, errtype, value, traceback):
        if self.bCDInto:
            os.chdir(self.OldCWD)
        if self.bPostDelete:
            TM.Delete(self.sPath)
