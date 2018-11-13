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
from TM_CommonPy._Logger import TMLog

class Counter:
    def __init__(self):
        self.iCount = 0

    def __call__(self):
        self.iCount += 1
        return self.iCount - 1

    def reset(self):
        self.__init__()
