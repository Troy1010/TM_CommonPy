from unittest import TestCase
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree


def __Copy(src,root_dst_dir):
    if os.path.isdir(src):
        for src_dir, dirs, files in os.walk(src):
            dst_dir = src_dir.replace(src, root_dst_dir, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.copy(src_file, dst_dir)
    elif os.path.isfile(src):
        dst_dir = src_dir.replace(src, root_dst_dir, 1)
        shutil.copy(src, dst_dir)
    else:
        print("__Copy\\Error\\src is not a valid file or directory")
__Copy('Examples_Backup','Examples')

try:
    import TM_CommonPy as TMC
except:
    sys.path.append(os.path.join(__file__,'..','..','..'))
    import TM_CommonPy as TMC



class Test_TM_CommonPy(TestCase):
    #?where to chdir?
    os.chdir(os.path.join('TM_CommonPy','tests'))
    sExampleXMLFile = os.path.join('Examples','ExampleXML.xml')
    sExampleXML_HasBOM = os.path.join('Examples','ExampleXML_HasBOM.xml')
    sExampleTXTFile = os.path.join('Examples','ExampleTXT.txt')

    def test_GetScriptRoot_IsString(self):
        s = TMC.GetScriptRoot()
        self.assertTrue(isinstance(s, str))

    def test_GetFileContent_IsString(self):
        s = TMC.GetFileContent(self.sExampleXMLFile)
        self.assertTrue(isinstance(s, str))

    def test_GetFileContent_ByExample(self):
        b = TMC.GetFileContent(self.sExampleTXTFile) == "I am example txt.\nHear me. Or, read me, rather."
        self.assertTrue(b)

    def test_GetFileContent_ByExample2(self):
        b = TMC.GetFileContent(self.sExampleTXTFile) == "I am example txt.\nHear me. Or, read me, maybe."
        self.assertTrue(not b)

    def test_GetXMLNamespaces_ByExample(self):
        b = str(TMC.GetXMLNamespaces(self.sExampleXMLFile)) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}'
        self.assertTrue(b)

    def test_GetXMLNamespaces_ByExample_HasBOM(self):
        b = str(TMC.GetXMLNamespaces(self.sExampleXML_HasBOM)) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}'
        self.assertTrue(b)

    def test_Copy_ByExample(self):
        TMC.Copy('Examples','Examples_TmpCopy')
        b = False
        if os.path.isfile(os.path.join('Examples_TmpCopy','ExampleXML.xml')) and os.path.isfile(os.path.join('Examples_TmpCopy','ExampleTXT.txt')):
            b = True
        shutil.rmtree('Examples_TmpCopy')
        self.assertTrue(b)

    def test_FindElem(self):
        #---Open
        TMC.Copy('Examples','Examples_FindElem')
        #---
        vTree = xml.etree.ElementTree.parse(os.path.join('Examples_FindElem','ExampleXML.xml'))
        vElemToFind = xml.etree.ElementTree.Element("ProjectConfiguration", Include="Debug|Win32")
        vFoundElem = TMC.FindElem(vElemToFind,vTree)
        self.assertTrue(vFoundElem[0].tag == "{http://schemas.microsoft.com/developer/msbuild/2003}Configuration" and vFoundElem[0].text == "Debug")
        self.assertTrue(vFoundElem[1].tag == "{http://schemas.microsoft.com/developer/msbuild/2003}Platform" and vFoundElem[1].text == "Win32")
        #---Close
        shutil.rmtree('Examples_FindElem')

    def test_FindElem_FindNothing(self):
        #---Open
        TMC.Copy('Examples','Examples_FindElem')
        #---
        vTree = xml.etree.ElementTree.parse(os.path.join('Examples_FindElem','ExampleXML.xml'))
        vElemToFind = xml.etree.ElementTree.Element("asdffdasfsdfg", Include="sfghdghrtd")
        vFoundElem = TMC.FindElem(vElemToFind,vTree)
        self.assertTrue(vFoundElem is None)
        #---Close
        shutil.rmtree('Examples_FindElem')


    #---GetDictCount
    def test_GetDictCount_ByExample(self):
        cDict = {"age":25,"blue":3,"cat":5}
        self.assertTrue(TMC.GetDictCount(cDict) == 3)

    #------Extra tests
    def test_Does_And_ShortCircuit(self):
        dict1 = {"zeed":1,"beep":2}
        for vKey,vValue in dict1.items():
            if "boop" in dict1 and dict1["boop"] == 1:
                pass
