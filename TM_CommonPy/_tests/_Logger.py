import os
import logging
import TM_CommonPy as TM
# Settings
bWriteLogFile = True
sLogFile = os.path.join(__file__, '..', 'TMLog_LogTests.log')
vMasterThreshold = logging.DEBUG
vConsoleHandlerThreshold = logging.WARNING
vFileHandlerThreshold = logging.DEBUG

TMLog_LogTests = logging.getLogger(__name__)
TMLog_LogTests.info = TM.LoggingHeaderDecorator(TMLog_LogTests.info)
TMLog_LogTests.debug = TM.LoggingHeaderDecorator(TMLog_LogTests.debug)
TMLog_LogTests.setLevel(vMasterThreshold)
vFormatter = logging.Formatter('%(message)s')
# ---ConsoleHandler
vConsoleHandler = logging.StreamHandler()
vConsoleHandler.setLevel(vConsoleHandlerThreshold)
vConsoleHandler.setFormatter(vFormatter)
TMLog_LogTests.addHandler(vConsoleHandler)
# ---FileHandler
try:
    os.remove(sLogFile)
except (PermissionError, FileNotFoundError):
    pass
if bWriteLogFile:
    bLogFileIsOpen = False
    try:
        os.rename(sLogFile, sLogFile)
    except PermissionError:
        bLogFileIsOpen = True
    except FileNotFoundError:
        pass
    if not bLogFileIsOpen:
        vFileHandler = logging.FileHandler(sLogFile)
        vFileHandler.setFormatter(vFormatter)
        vFileHandler.setLevel(vFileHandlerThreshold)
        TMLog_LogTests.addHandler(vFileHandler)
