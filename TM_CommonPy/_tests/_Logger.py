import os, logging
##region Settings
bWriteLogFile = True
sLogFile = os.path.join(__file__,'..','TMLog_LogTests.log')
vMasterThreshold = logging.DEBUG
vConsoleHandlerThreshold = logging.WARNING
vFileHandlerThreshold = logging.DEBUG
##endregion
import TM_CommonPy as TM

class HeaderDecorator:
    """Decorator to add a header"""
    def __init__(self,method):
        self.method=method
        self.sLastFnName=""
        self.bFirstCall=True
    def __call__(self,*args,**kwargs):
        if self.sLastFnName != TM.FnName(1):
            self.sLastFnName = TM.FnName(1)
            if self.bFirstCall:
                self.bFirstCall=False
                self.method("-------"+TM.FnName(1))
            else:
                self.method("\n\n-------"+TM.FnName(1))
        self.method(*args,**kwargs)

TMLog_LogTests = logging.getLogger(__name__)
TMLog_LogTests.info = HeaderDecorator(TMLog_LogTests.info)
TMLog_LogTests.debug = HeaderDecorator(TMLog_LogTests.debug)
TMLog_LogTests.setLevel(vMasterThreshold)
vFormatter = logging.Formatter('%(message)s')
#---ConsoleHandler
vConsoleHandler = logging.StreamHandler()
vConsoleHandler.setLevel(vConsoleHandlerThreshold)
vConsoleHandler.setFormatter(vFormatter)
TMLog_LogTests.addHandler(vConsoleHandler)
#---FileHandler
try:
    os.remove(sLogFile)
except (PermissionError,FileNotFoundError):
    pass
if bWriteLogFile:
    bLogFileIsOpen = False
    try:
        os.rename(sLogFile,sLogFile)
    except PermissionError:
        bLogFileIsOpen = True
    except FileNotFoundError:
        pass
    if not bLogFileIsOpen:
        vFileHandler = logging.FileHandler(sLogFile)
        vFileHandler.setFormatter(vFormatter)
        vFileHandler.setLevel(vFileHandlerThreshold)
        TMLog_LogTests.addHandler(vFileHandler)
