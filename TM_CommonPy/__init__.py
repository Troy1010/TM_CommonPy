##region Settings
bWriteLog=True
##endregion

__version__ = '0.10.0'
#__all__ = ["CommandSet"]
##region LogInit
import logging, os
TMLog = logging.getLogger('TM_CommonPy')
bPermissionError = False
if bWriteLog:
    sLogFile = os.path.join(__file__,'..','TMLog.log')
    if os.path.exists(sLogFile):
        try:
            os.remove(sLogFile)
        except PermissionError:
            bPermissionError = True
    TMLog.addHandler(logging.FileHandler(sLogFile))
    if bPermissionError:
        TMLog.debug("Could not remove TMLog due to PermissionError")
##endregion
##region ImportThisModule
import TM_CommonPy as TM
from TM_CommonPy.Misc import *
from TM_CommonPy.CommandSet import CommandSet
from TM_CommonPy.CopyContext import CopyContext
from TM_CommonPy.ElementTreeContext import ElementTreeContext
import TM_CommonPy.Narrator
##endregion
