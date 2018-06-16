import os, sys
import importlib
import pip
import xml.etree.ElementTree
import shutil
import subprocess
import shlex
import stat
import importlib
import pkgutil
import inspect
import importlib.util
import TM_CommonPy.Narrator
import ctypes
import TM_CommonPy as TM
from TM_CommonPy import TMLog


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
    return cReturning

def GetRecommendedIntegrationsPair(sRoot):
    if os.path.isdir(os.path.join(sRoot,"RecommendedIntegration")):
        sys.path.insert(0,sRoot)
        import RecommendedIntegration
        if not hasattr(RecommendedIntegration,"Main"):
            raise AttributeError("RecommendedIntegration.Main")
        if not hasattr(RecommendedIntegration,"Main_Undo"):
            raise AttributeError("RecommendedIntegration.Main_Undo")
        return (RecommendedIntegration.Main,RecommendedIntegration.Main_Undo)

def QueRecommendedIntegrations(vCommandSet,sConanBuildInfoTxtFile):
    for sRoot in TM.Conan.GetDependencyRoots(sConanBuildInfoTxtFile):
        vDoUndoPair = TM.Conan.GetRecommendedIntegrationsPair(sRoot)
        if not vDoUndoPair is None:
            vCommandSet.Que(TM.Conan.GetRecommendedIntegrationsPair(sRoot),sRoot)
