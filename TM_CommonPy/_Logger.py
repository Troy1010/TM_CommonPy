import os
import logging
# Settings
bWriteLogFile = True
sLogFile = os.path.join(__file__, '..', 'TMLog.log')
vMasterThreshold = logging.DEBUG
vConsoleHandlerThreshold = logging.WARNING
vFileHandlerThreshold = logging.DEBUG

TMLog = logging.getLogger(__name__)
TMLog.setLevel(vMasterThreshold)
vFormatter = logging.Formatter('%(levelname)-7s %(message)s')
# Handlers
if len(logging.getLogger().handlers):  # Default handlers are empty when it's the weird nosetests extra run.
    # ---FileHandler
    try:
        os.remove(sLogFile)
    except FileNotFoundError:
        pass
    if bWriteLogFile:
        vFileHandler = logging.FileHandler(sLogFile)
        vFileHandler.setFormatter(vFormatter)
        vFileHandler.setLevel(vFileHandlerThreshold)
        TMLog.addHandler(vFileHandler)
    # ---ConsoleHandler
    vConsoleHandler = logging.StreamHandler()
    vConsoleHandler.setLevel(vConsoleHandlerThreshold)
    vConsoleHandler.setFormatter(vFormatter)
    TMLog.addHandler(vConsoleHandler)
