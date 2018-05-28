import os, sys
import importlib
import pip
import xml.etree.ElementTree
import shutil
import subprocess


#beta
#Maybe use __file__ instead?
def GetScriptRoot():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def GetFileContent(sFile):
    vFile = open(sFile,'r')
    sContent = vFile.read()
    vFile.close()
    return sContent

#Works fine for non-BOM XML files.. but runs into trouble otherwise.
def GetXMLNamespaces(sXMLFile):
    cNamespaces = dict([
        node for _, node in xml.etree.ElementTree.iterparse(
            sXMLFile, events=['start-ns']
        )
    ])
    return cNamespaces

def Copy(sSrcDir,sDstDir,bPreDelete=False):
    if bPreDelete:
        TryDeleteFolder(sDstDir)
    if os.path.isdir(sSrcDir):
        for src_dir, dirs, files in os.walk(sSrcDir):
            dst_dir = src_dir.replace(sSrcDir, sDstDir, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.copy(src_file, dst_dir)
    elif os.path.isfile(sSrcDir):
        dst_dir = src_dir.replace(sSrcDir, sDstDir, 1)
        shutil.copy(sSrcDir, dst_dir)
    else:
        print("Copy|Error|sSrcDir "+sSrcDir+" is not a valid file or directory")

def GetDictCount(cDict):
    return len(cDict.values())

#alpha
def IsEmpty(cCollection):
    #---None
    if cCollection is None:
        return True
    #---Dict
    if isinstance(cCollection,dict):
        cCollection = cCollection.items()
    #---NotACollection
    try:
        for vKey,vValue in cCollection:
            pass
    except:
        return True
    #---Empty
    if len(cCollection) ==0:
        return True


#beta
def FindElem(vElemToFind,vTreeToSearch):
    for vElem in vTreeToSearch.iter():
        bFound = True
        #-tag or text differences?
        if not (vElemToFind.tag in vElem.tag and ((vElemToFind.text == vElem.text) or (vElemToFind.text is None))):
            bFound = False
            continue
        #-attrib differences?
        for vKey,vValue in vElemToFind.attrib.items():
            if not ((vKey in vElem.attrib) and (vElem.attrib[vKey] == vValue)):
                bFound = False
                break
        if not bFound:
            continue
        #-child differences?
        for vElemToFindChild in vElemToFind:
            if FindElem(vElemToFindChild,vElem) is None:
                bFound = False
                break
        #-If there are still no differences, we found it. Return the element
        if bFound:
            return vElem
    #-Couldn't find
    return

#dev
def RunPowerShellScript(sScriptFile):
    vProcess = subprocess.Popen(["powershell.exe","-executionpolicy ","bypass","-file",sScriptFile], shell=True)
    vProcess.communicate()
    return vProcess

#dev
def TryDeleteFolder(sFileOrDir):
    if os.path.isdir(sFileOrDir):
        shutil.rmtree(sFileOrDir)
    elif os.path.exists(sFileOrDir):
        os.remove(sFileOrDir)

#dev
def TryMakeDirs(sDir):
    if not os.path.exists(sDir):
        os.makedirs(sDir)

#dev
def InstallAndImport(package):
    try:
        importlib.import_module(package)
    except ImportError:
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)
