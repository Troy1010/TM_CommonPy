##region Settings
bWriteLog=True
##endregion

__version__ = '0.10.0'
#__all__ = ["CommandSet"]
##region LogInit
import logging, os
TMLog = logging.getLogger('TM_CommonPy')
if bWriteLog:
    sLogFile = os.path.join(__file__,'..','TMLog.log')
    if os.path.exists(sLogFile):
        os.remove(sLogFile)
    TMLog.addHandler(logging.FileHandler(sLogFile))
##endregion
##region ImportThisModule
import TM_CommonPy as TM
from TM_CommonPy.Misc import *
from TM_CommonPy.CommandSet import CommandSet
from TM_CommonPy.CopyContext import CopyContext
from TM_CommonPy.ElementTreeContext import ElementTreeContext
import TM_CommonPy.Narrator
import TM_CommonPy.Conan
##endregion
