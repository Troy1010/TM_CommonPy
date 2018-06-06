import unittest
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree

import TM_CommonPy as TM
import TM_CommonPy.Narrator as TM_NAR

#legacy
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

class TestObj():
    Name = "TestObject"

    def Method(self):
        print("Hiii I'm the Test Object")

    def TypeMethod(self):
        print("Hiii I'm the Test Object")

class Test_TM_CommonPy(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('TM_CommonPy','tests'))
        TM.Copy('Examples_Backup','Examples_Shared')
        os.chdir('Examples_Shared')

    @classmethod
    def tearDownClass(self):
        os.chdir('..')
        shutil.rmtree('Examples_Shared')
        os.chdir(os.path.join('..','..'))

    def setUp(self):
        self.sExampleXMLFile = 'ExampleXML.xml'
        self.sExampleXML_HasBOM = 'ExampleXML_HasBOM.xml'
        self.sExampleTXTFile = 'ExampleTXT.txt'
        pass

    def tearDown(self):
        pass

    #------Tests

    def test_GetScriptRoot_IsString(self):
        s = TM.GetScriptRoot()
        self.assertTrue(isinstance(s, str))

    def test_GetFileContent_IsString(self):
        s = TM.GetFileContent(self.sExampleXMLFile)
        self.assertTrue(isinstance(s, str))

    def test_GetFileContent_ByExample(self):
        self.assertEqual(TM.GetFileContent(self.sExampleTXTFile),"I am example txt.\nHear me. Or, read me, rather.")

    def test_GetFileContent_ByExample2(self):
        b = TM.GetFileContent(self.sExampleTXTFile) == "tyurityihghty"
        self.assertTrue(not b)

    def test_GetXMLNamespaces_ByExample(self):
        b = str(TM.GetXMLNamespaces(self.sExampleXMLFile)) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}'
        self.assertTrue(b)

    def test_GetXMLNamespaces_ByExample_HasBOM(self):
        b = str(TM.GetXMLNamespaces(self.sExampleXML_HasBOM)) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}'
        self.assertTrue(b)

    def test_FindElem(self):
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vElemToFind = xml.etree.ElementTree.Element("ProjectConfiguration", Include="Debug|Win32")
        vFoundElem = TM.FindElem(vElemToFind,vTree)
        self.assertTrue(vFoundElem[0].tag == "{http://schemas.microsoft.com/developer/msbuild/2003}Configuration" and vFoundElem[0].text == "Debug")
        self.assertTrue(vFoundElem[1].tag == "{http://schemas.microsoft.com/developer/msbuild/2003}Platform" and vFoundElem[1].text == "Win32")

    def test_FindElem_FindNothing(self):
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vElemToFind = xml.etree.ElementTree.Element("asdffdasfsdfg", Include="sfghdghrtd")
        vFoundElem = TM.FindElem(vElemToFind,vTree)
        self.assertTrue(vFoundElem is None)

    def test_Narrate_Elem(self):
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vRoot = vTree.getroot()
        print(TM_NAR.Narrate(vRoot))
        #self.assertTrue(False)

    def test_Narrate_Collection(self):
        cArray = [30,40,80,10]
        print(TM_NAR.Narrate(cArray))
        #self.assertTrue(False)

    def test_Narrate_Bool(self):
        print(TM_NAR.Narrate(True))
        print(TM_NAR.Narrate(False))
        #self.assertTrue(False)

    def test_Narrate_None(self):
        print(TM_NAR.Narrate(None))
        #self.assertTrue(False)

    def test_Narrate_UnknownObj(self):
        vObj = TestObj()
        print(TM_NAR.Narrate(vObj))
        #self.assertTrue(False)

    def test_Narrate_Object2(self):
        vObj = TestObj()
        print(TM_NAR.NarrateObject(vObj))
        print("========")
        print(TM_NAR.NarrateObject_Options(vObj, bMethodsStartFull=False, bExtrasStartFull=False))
        #self.assertTrue(False)

    #---GetDictCount
    def test_GetDictCount_ByExample(self):
        cDict = {"age":25,"blue":3,"cat":5}
        self.assertTrue(TM.GetDictCount(cDict) == 3)


    #------Extra tests
    def test_Does_And_ShortCircuit(self):
        dict1 = {"zeed":1,"beep":2}
        for vKey,vValue in dict1.items():
            if "boop" in dict1 and dict1["boop"] == 1:
                pass

    def test_CanYouKeyValueArrays(self):
        #array1 = [30,60,80,50]
        #for vKey, vValue in array1:
        #    print(str(vKey)+":"+str(vValue))
        pass

    def test_CanYouIterateNone(self):
        #vNone = None
        #for vChild in None:
        #    print("I'm alive!")
        pass

    def test_CanYouDelFromEmptyDict(self):
        #cDict = {}
        #del cDict["tre"]
        pass

    def test_GetFileStrings(self):
        # print('start..')
        # for sFileName in TM.GetFileNames("."):
        #     print("sFileName:"+sFileName)
        print(TM.Narrator.Narrate(TM.GetRelFileNames(".")))
        #self.assertTrue(False)

    def test_ListFiles(self):
        print(TM.ListFiles("."))
#        self.assertTrue(False)

class Test_TM_CommonPy_CopyExamples(unittest.TestCase):
    bDontDelete=False

    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('TM_CommonPy','tests'))

    @classmethod
    def tearDownClass(self):
        os.chdir(os.path.join('..','..'))

    def setUp(self):
        self.sExampleXMLFile = 'ExampleXML.xml'
        self.sExampleXML_HasBOM = 'ExampleXML_HasBOM.xml'
        self.sExampleTXTFile = 'ExampleTXT.txt'
        self.sCurrentResFolder = 'Examples__'+self.id()[self.id().rfind("test_")+5:]
        TM.Copy('Examples_Backup',self.sCurrentResFolder, bPreDelete = True)
        os.chdir(self.sCurrentResFolder)

    def tearDown(self):
        os.chdir('..')
        if not self.bDontDelete:
            TM.Delete(self.sCurrentResFolder)
        else:
            self.bDontDelete = False

    #------Tests

    def test_RunPowershellScript_Try(self):
        print(os.path.join(os.getcwd(),'HelloWorld.ps1'))
        TM.RunPowerShellScript(os.path.join(os.getcwd(),'HelloWorld.ps1'))
        #TM.RunPowershellScript('HelloWorld.ps1')
        #self.assertTrue(False)

    def test_Run(self):
        TM.Run("git clone -b beta https://github.com/Troy1010/TM_CommonCPP.git")

    def test_GitPullOrClone(self):
        TM.GitPullOrClone("https://github.com/Troy1010/TM_CommonCPP.git")

    def test_CopyExclude(self):
        TM.Copy("Folder2","FolderCopied",sExclude="XML")
        #self.bDontDelete = True
