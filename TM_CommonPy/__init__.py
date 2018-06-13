##region Settings
bWriteLog=True
##endregion

__version__ = '0.10.0'
#__all__ = ["CommandSet"]
##region ImportThisModule
import TM_CommonPy as TM
from TM_CommonPy.Misc import *
from TM_CommonPy.CommandSet import CommandSet
from TM_CommonPy.CopyContext import CopyContext
from TM_CommonPy.ElementTreeContext import ElementTreeContext
##endregion
##region Log init
import logging, os
TMLog = logging.getLogger('TM_CommonPy')
if bWriteLog:
    sLogFile = os.path.join(__file__,'..','TMLog.log')
    TM.Delete(sLogFile)
    TMLog.addHandler(logging.FileHandler(sLogFile))
##endregion
