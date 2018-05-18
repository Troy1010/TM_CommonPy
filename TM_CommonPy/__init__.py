import os, sys
import io
import importlib
import pip
import xml.etree.ElementTree

#Maybe use __file__ instead?
def GetScriptRoot():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def GetFileContent(sFile):
    with open(sFile,'r') as f:
        sContent = f.read()
    return sContent

def GetXMLNamespaces(sXMLFile):
    cNamespaces = dict([
        node for _, node in xml.etree.ElementTree.iterparse(
            io.StringIO(GetFileContent(sXMLFile)), events=['start-ns']
        )
    ])
    return cNamespaces

#not tested
def TryMakeDirs(sDir):
    if not os.path.exists(sDir):
        os.makedirs(sDir)

#not tested
def copyanything(root_src_dir,root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)

#not tested
def InstallAndImport(package):
    try:
        importlib.import_module(package)
    except ImportError:
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)
