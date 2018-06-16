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

#beta
class CommandSet:
    def __init__(self):
        self.PreviousCommandSet = []
        self.CommandSet = []
    def Que(self,cDoUndoPair,cArgs):
        if len(cDoUndoPair) != 2:
            raise ValueError(self.__class__.__name__+"::"+TM.FnName()+"`first arg must be a container of 2 methods: Do and Undo")
        if not TM.IsCollection(cArgs):
            cArgs = [cArgs]
        self.CommandSet.append([cDoUndoPair,cArgs])
    def Execute(self,bRedo=False):
        if bRedo:
            #---Undo what is in PreviousCommandSet
            for vItem in self.PreviousCommandSet:
                TMLog.debug(self.__class__.__name__+"::"+TM.FnName()+"`Reundo:"+str(vItem[0]))
                self._Undo(vItem[0],vItem[1])
        else:
            #---Undo what is in PreviousCommandSet but not CommandSet
            for vItem in [x for x in self.PreviousCommandSet if x not in self.CommandSet]:
                TMLog.debug(self.__class__.__name__+"::"+TM.FnName()+"`Undo:"+str(vItem[0]))
                self._Undo(vItem[0],vItem[1])
        if bRedo:
            #---Do what is in CommandSet
            for vItem in self.CommandSet:
                TMLog.debug(self.__class__.__name__+"::"+TM.FnName()+"`Redo:"+str(vItem[0]))
                self._Do(vItem[0],vItem[1])
        else:
            #---Do what is in CommandSet but not PreviousCommandSet
            for vItem in [x for x in self.CommandSet if x not in self.PreviousCommandSet]:
                TMLog.debug(self.__class__.__name__+"::"+TM.FnName()+"`Do:"+str(vItem[0]))
                self._Do(vItem[0],vItem[1])
        #---
        self.PreviousCommandSet = self.CommandSet
        self.CommandSet = []
    @staticmethod
    def _Do(cDoUndoPair,cArgs):
        cDoUndoPair[0](*cArgs)
    @staticmethod
    def _Undo(cDoUndoPair,cArgs):
        cDoUndoPair[1](*cArgs)