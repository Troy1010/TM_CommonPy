import os
import sys
import importlib
import importlib.util
import pip
import xml.etree.ElementTree
import shutil
import subprocess
import shlex
import stat
import pkgutil
import inspect
import ctypes
import types
import traceback
from TM_CommonPy._Logger import TMLog  # noqa


def Hello():
    print("running Hello")
    TMLog.debug("Hello")


def Ceil(value, ndigits=0):
    return round(value*10**ndigits + 0.5)/10**ndigits


def RemoveWhitespace(s):
    return "".join(s.split())


def GetNumsInString(sString):
    cNums = []
    sNum = ""
    for vChar in sString:
        if vChar.isdigit() or vChar == ".":
            sNum += vChar
        elif sNum:
            cNums.append(float(sNum))
            sNum = ""
    if sNum:  # Just in case the string ended at a num.
        cNums.append(float(sNum))
    return cNums


def DisplayDone():
    print("\n\t\t\tDone\n")
    os.system('pause')


def StringizeException(e):
    s = ("===================================================================="
         + "\nTraceback (most recent call last):\n"
         + ''.join(traceback.format_tb(e.__traceback__))
         + "\n" + type(e).__name__ + ": " + str(e)
         )
    return s


def DisplayException(e):
    print("====================================================================")
    print("Traceback (most recent call last):")
    traceback.print_tb(e.__traceback__)
    print(type(e).__name__ + ": " + str(e))
    os.system('pause')


def TryMkdir(sPath):
    try:
        os.mkdir(sPath)
    except FileExistsError:
        pass

# Maybe use __file__ instead?


def GetScriptRoot():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def GetFileContent(sFilePath):
    vFile = open(sFilePath, 'r')
    sContent = vFile.read()
    vFile.close()
    return sContent


def GetXMLNamespaces(sXMLFile):
    cNamespaces = dict([
        node for _, node in xml.etree.ElementTree.iterparse(
            sXMLFile, events=['start-ns']
        )
    ])
    return cNamespaces


def GetRelFileNames(sDir):
    cFileNames = []
    for root, dirs, files in os.walk(sDir):
        sRelPath = root.replace(sDir, '')
        for f in files:
            cFileNames.append(os.path.join(sRelPath, f))
    return cFileNames


def GetFullFileNames(sDir):
    cFileNames = []
    for root, dirs, files in os.walk(sDir):
        for f in files:
            cFileNames.append(os.path.abspath(f))
    return cFileNames


def Copy(sSrc, sDstDir, bPreDelete=False, sExclude="", bCDInto=False):
    # ---PreDelete
    if bPreDelete:
        Delete(sDstDir)
    # ---Dir
    if os.path.isdir(sSrc):
        for sRoot, cDirs, cFiles in os.walk(sSrc):
            dst_dir = sRoot.replace(sSrc, sDstDir, 1)
            if not os.path.exists(dst_dir):
                if not (sExclude != "" and sExclude in dst_dir):
                    os.makedirs(dst_dir)
            for file_ in cFiles:
                src_file = os.path.join(sRoot, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                if not (sExclude != "" and sExclude in src_file):
                    shutil.copy(src_file, dst_dir)
    # ---File
    elif os.path.isfile(sSrc):
        if not (sExclude != "" and sExclude in sSrc):
            shutil.copy(sSrc, sDstDir)
    else:
        raise OSError("sSrc:"+sSrc+" is not a valid file or directory")
    # ---bCDInto
    if bCDInto:
        os.chdir(sDstDir)


def IsEmpty(cCollection):
    # ---None
    if cCollection is None:
        return True
    # ---Dict
    if isinstance(cCollection, dict):
        cCollection = cCollection.items()
    # ---NotACollection
    if not IsCollection(cCollection):
        return True
    # ---Empty
    if len(cCollection) == 0:
        return True
    return False


def FindElem(vElemToFind, vTreeToSearch):
    for vElem in vTreeToSearch.iter():
        bFound = True
        # -tag or text differences?
        if not (vElemToFind.tag in vElem.tag and ((vElemToFind.text == vElem.text) or (vElemToFind.text is None))):
            bFound = False
            continue
        # -attrib differences?
        for vKey, vValue in vElemToFind.attrib.items():
            if not ((vKey in vElem.attrib) and (vElem.attrib[vKey] == vValue)):
                bFound = False
                break
        if not bFound:
            continue
        # -child differences?
        for vElemToFindChild in vElemToFind:
            if FindElem(vElemToFindChild, vElem) is None:
                bFound = False
                break
        # -If there are still no differences, we found it. Return the element
        if bFound:
            return vElem
    # -Couldn't find
    return None


def AppendElemIfAbsent(vElemToAppend, vElemToAppendTo):
    if FindElem(vElemToAppend, vElemToAppendTo) is None:
        vElemToAppendTo.append(vElemToAppend)


def RemoveElem(vElemToRemoveTemplate, vElemToRemoveFrom):
    vElemToRemove = FindElem(vElemToRemoveTemplate, vElemToRemoveFrom)
    if vElemToRemove is not None:
        vElemToRemoveFrom.remove(vElemToRemove)


def IsCollection(vVar):
    """Does not include strings as a collection"""
    try:
        iter(vVar)
    except TypeError:
        bCanIter = False
    else:
        bCanIter = True
    return bCanIter and not isinstance(vVar, str)


IsIterable = IsCollection


def PrintAndQuit(e):
    print(StringizeException(e))
    sys.exit(0)


def WithinRange(value, min_, max_):
    if value < min_:
        return min_
    elif value > max_:
        return max_
    else:
        return value


class Hook:
    def __init__(self, *args, on_error=None, bPrintAndQuitOnError=False):
        self.cHandlers = []
        self.on_error = on_error
        self.bPrintAndQuitOnError = bPrintAndQuitOnError
        for arg in args:
            if not IsIterable(arg):
                self.cHandlers.append(arg)
            else:
                self.cHandlers.extend(arg)

    def __call__(self, *args, **kwargs):
        for vHandler in self.cHandlers:
            if callable(vHandler):
                try:
                    vHandler(*args, **kwargs)
                except Exception as e:
                    if self.on_error:
                        self.on_error(e)
                    if self.bPrintAndQuitOnError:
                        PrintAndQuit(e)
                    raise


def RunPowerShellScript(sScriptFile):
    vProcess = subprocess.Popen(
        ["powershell.exe", "-executionpolicy ", "bypass", "-file", sScriptFile], shell=True)
    vProcess.communicate()
    return vProcess

# Currently, passing a string to subprocess.run will fail on linux (if shell=false) because lunix believes the first item is a param.
# To get around this, this function uses shlex to split the string  and pass it as a collection instead.
# More info here:https://codecalamity.com/run-subprocess-run/#arguments-as-string-or-list


def Run(sToRun):
    subprocess.run(shlex.split(sToRun, posix=False))


def Delete(sFilePathOrDir):
    if os.path.isdir(sFilePathOrDir):
        # -Change mode of all files to Write
        for root, dirs, files in os.walk(sFilePathOrDir):
            for sFilePath in files:
                os.chmod(os.path.join(root, sFilePath), stat.S_IWRITE)
        # -
        shutil.rmtree(sFilePathOrDir)
    elif os.path.exists(sFilePathOrDir):
        os.remove(sFilePathOrDir)


def MakeDir(sDir, bCDInto=False):
    if not os.path.exists(sDir):
        os.makedirs(sDir)
    if bCDInto:
        os.chdir(sDir)


def ListFiles(sDir):
    sReturning = ""
    for root, dirs, files in os.walk(sDir):
        level = root.replace(sDir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        sReturning += "\n" + '{}{}/'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            sReturning += "\n" + '{}{}'.format(subindent, f)
    return sReturning


class fragile():
    class Break(Exception):
        """Break out of the with statement"""

    def __init__(self, value):
        self.value = value

    def __enter__(self):
        return self.value.__enter__()

    def __exit__(self, etype, value, traceback):
        error = self.value.__exit__(etype, value, traceback)
        if etype == self.Break:
            return True
        return error

# This function allows you to import a file witout poluting sys.path


def ImportFromDir(sFilePath):
    # ---Determine sModuleName
    sModuleName = os.path.split(sFilePath)[1]
    if sModuleName[-3:] == ".py":
        sModuleName = sModuleName[:-3]
    # ---Get vModule
    vSpec = importlib.util.spec_from_file_location(sModuleName, sFilePath)
    if vSpec is None:
        raise ValueError("ImportFromDir`Could not retrieve spec. \nsModuleName:"
                         + sModuleName+"\nsFilePath:"+sFilePath+"\nCurrentWorkingDir:"+os.getcwd())
    vModule = importlib.util.module_from_spec(vSpec)
    # ---Execute vModule
    vSpec.loader.exec_module(vModule)
    # ---
    return vModule


def InstallAndImport(package):
    try:
        importlib.import_module(package)
    except ImportError:
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


def TryGetCollectionAttrib(vObject, sAttribName):
    if hasattr(vObject, sAttribName):
        return getattr(vObject, sAttribName)
    return []


def MsgBox(sMsg, iStyle=1):
    return ctypes.windll.user32.MessageBoxW(0, sMsg, FnName(1), iStyle)


def FnName(iShift=0):
    return inspect.stack()[1+iShift][3]


def IsTextInFile(sText, sFilePath):
    try:
        with open(sFilePath, 'r') as vFile:
            return sText in vFile.read()
    except UnicodeDecodeError:
        with open(sFilePath, 'rb') as vFile:
            return sText in "".join(map(chr, vFile.read()))


def ImportSubmodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(ImportSubmodules(full_name))
    return results


def CopyFunction(vFunction):
    return types.FunctionType(vFunction.__code__, vFunction.__globals__, vFunction.__name__, vFunction.__defaults__, vFunction.__closure__)
