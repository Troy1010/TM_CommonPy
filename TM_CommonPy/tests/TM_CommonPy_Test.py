##region Settings
bPostDelete = False
bWriteLog = True
##endregion

import unittest
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree

import TM_CommonPy as TM
import VisualStudioAutomation as VS
#import TM_CommonPy.Narrator as TM.Narrator

##region LogInit
import logging, os
TMLog_Tests = logging.getLogger('TM_CommonPy_Tests')
if bWriteLog:
    sLogFile = os.path.join(__file__,'..','TMLog_Tests.log')
    if os.path.exists(sLogFile):
        os.remove(sLogFile)
    TMLog_Tests.addHandler(logging.FileHandler(sLogFile))
##endregion

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

class Te5tObj():
    Name = "Te5tObject"

    def Method(self):
        print("Hiii I'm the Test Object")

    def TypeMethod(self):
        print("Hiii I'm the Test Object")

class Test_TM_CommonPy_SameFolder(unittest.TestCase):
    sTestWorkspace = "TestWorkspace_SameFolder/"
    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('TM_CommonPy','tests'))
        TM.Copy("res/Examples_Backup",self.sTestWorkspace,bPreDelete=True)
        self.OldCWD = os.getcwd()
        os.chdir(self.sTestWorkspace)

    @classmethod
    def tearDownClass(self):
        os.chdir(self.OldCWD)
        global bPostDelete
        if bPostDelete:
            TM.Delete(self.sTestWorkspace)
        os.chdir(os.path.join('..','..'))

    #------Tests



    def test_GetScriptRoot_IsString(self):
        s = TM.GetScriptRoot()
        self.assertTrue(isinstance(s, str))

    def test_GetFileContent_IsString(self):
        s = TM.GetFileContent('ExampleXML.xml')
        self.assertTrue(isinstance(s, str))

    def test_GetFileContent_ByExample(self):
        self.assertEqual(TM.GetFileContent('ExampleTXT.txt'),"I am example txt.\nHear me. Or, read me, rather.")

    def test_GetFileContent_ByExample2(self):
        b = TM.GetFileContent('ExampleTXT.txt') == "tyurityihghty"
        self.assertTrue(not b)

    def test_GetXMLNamespaces_ByExample(self):
        b = str(TM.GetXMLNamespaces('ExampleXML.xml')) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}'
        self.assertTrue(b)

    def test_GetXMLNamespaces_ByExample_HasBOM(self):
        b = str(TM.GetXMLNamespaces('ExampleXML_HasBOM.xml')) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}'
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
        print(TM.Narrator.Narrate(vRoot))
        #self.assertTrue(False)

    def test_Narrate_Collection(self):
        cArray = [30,40,80,10]
        print(TM.Narrator.Narrate(cArray))
        #self.assertTrue(False)

    def test_Narrate_Bool(self):
        print(TM.Narrator.Narrate(True))
        print(TM.Narrator.Narrate(False))
        #self.assertTrue(False)

    def test_Narrate_None(self):
        print(TM.Narrator.Narrate(None))
        #self.assertTrue(False)

    def test_Narrate_UnknownObj(self):
        vObj = Te5tObj()
        print(TM.Narrator.Narrate(vObj))
        #self.assertTrue(False)

    def test_Narrate_Object2(self):
        vObj = Te5tObj()
        print(TM.Narrator.NarrateObject(vObj))
        print("========")
        print(TM.Narrator.NarrateObject_Options(vObj, bMethodsStartFull=False, bExtrasStartFull=False))
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

    def test_IsCollection(self):
        self.assertTrue(TM.IsCollection(["beep","boop"]))
        self.assertFalse(TM.IsCollection("beep"))

class Test_TM_CommonPy(unittest.TestCase):
    sTestWorkspace = "TestWorkspace/"
    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('TM_CommonPy','tests'))
        TM.Delete(self.sTestWorkspace)

    @classmethod
    def tearDownClass(self):
        os.chdir(os.path.join('..','..'))
        global bPostDelete
        if bPostDelete:
            TM.Delete(self.sTestWorkspace)

    #------Tests
    def test_RunPowershellScript_Try(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            TM.RunPowerShellScript(os.path.join(os.getcwd(),'HelloWorld.ps1'))

    def test_Run(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            TM.Run("git clone -b beta https://github.com/Troy1010/TM_CommonCPP.git")

    def test_GitPullOrClone(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            TM.GitPullOrClone("https://github.com/Troy1010/TM_CommonCPP.git")

    def test_CopyExclude(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            TM.Copy("Folder2","FolderCopied",sExclude="XML")

    def test_CommandSet(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            #-Pre-checking just to be sure test is set up correctly
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            #-
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([VS.IntegrateProps,VS.IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])
            vCommandSet.Execute()
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertTrue("conanbuildinfo.props" in vHelloWorldFile.read())

    def test_CommandSet2(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            #-Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            #-
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([VS.IntegrateProps,VS.IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])
            vCommandSet.Execute()
            #-Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertTrue("conanbuildinfo.props" in vHelloWorldFile.read())
            #-
            vCommandSet.Execute()
            #-Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())

    def test_CommandSet3(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            #---Open
            TM.Copy("HelloWorld.vcxproj","HelloWorld_Clean.vcxproj")
            #---
            #-Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            #-
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([VS.IntegrateProps,VS.IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])
            vCommandSet.Execute()
            #-Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertTrue("conanbuildinfo.props" in vHelloWorldFile.read())
            #-
            TM.Copy("HelloWorld_Clean.vcxproj","HelloWorld.vcxproj")
            #-Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            #-
            vCommandSet.Que([VS.IntegrateProps,VS.IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])
            vCommandSet.Execute()
            #-Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            #-
            vCommandSet.Que([VS.IntegrateProps,VS.IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])
            vCommandSet.Execute(bRedo=True)
            #-Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertTrue("conanbuildinfo.props" in vHelloWorldFile.read())
            #-

    def test_CommandSet_ValueError(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            vCommandSet = TM.CommandSet()
            with self.assertRaises(ValueError):
                vCommandSet.Que([VS.IntegrateProps,VS.IntegrateProps_Undo,VS.IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])

    def test_CommandSet_SingleArg(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([TM.IsCollection,TM.IsCollection],"Project.vcxproj")
            vCommandSet.Execute()

    def test_GetDependencyRoots(self):
        TMLog_Tests.debug("\n\n-------"+TM.FnName())
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            for sRoot in TM.Conan.GetDependencyRoots("conanbuildinfo.txt"):
                TMLog_Tests.debug(sRoot)
