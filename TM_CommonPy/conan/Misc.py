from TM_CommonPy._Logger import TMLog
import TM_CommonPy as TM

def GetDependencyRoots(sConanBuildInfoTxtFile):
    bRootIsNext = False
    with open(sConanBuildInfoTxtFile,'r') as vFile:
        cReturning = []
        for sLine in vFile:
            if "[rootpath_" in sLine:
                bRootIsNext = True
                continue
            if bRootIsNext:
                bRootIsNext = False
                cReturning.append(sLine.strip())
    TMLog.debug("GetDependencyRoots`cReturning:"+TM.Narrator.Narrate(cReturning))
    return cReturning
