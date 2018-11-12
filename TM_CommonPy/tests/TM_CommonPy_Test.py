import os
##region Settings
bPostDelete = False
bWriteLog = True
sLogFile = os.path.join(__file__,'..','TMLog_Tests.log')
bWriteLog = True
##endregion

import unittest
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree
import openpyxl

import TM_CommonPy as TM
import TM_CommonPy.openpyxl
import VisualStudioAutomation as VS
import dill
import importlib

##region LogInit
import logging
TMLog_Tests = logging.getLogger(__name__)
TMLog_Tests.setLevel(logging.DEBUG)
try:
    os.remove(sLogFile)
except (PermissionError,FileNotFoundError):
    pass
if bWriteLog:
    bLogFileIsOpen = False
    try:
        os.rename(sLogFile,sLogFile)
    except PermissionError:
        bLogFileIsOpen = True
    except FileNotFoundError:
        pass
    if not bLogFileIsOpen:
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
    def test_RemoveWhitespace(self):
        s = b'<td>\n\t\t\t\t\t\t\t\t\t<span class="label">Hometown/High School:</span>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t    \t     \t      \n    \t    \t\t    \t\t\t    \t\t\t    \t    \t\t    \t\t\t\t\t\t\t\t\tNew Berlin, Wis.\n\t\t        \t\t    \t\t\t    \t\t\t\t/\n    \t\t\t    \t\t\t    \t    \t\t    \t\t\t\t\t\t\t\t\tEisenhower\n\t\t        \t\t    \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t\t    \t\t\t\t\t    \t\t\t\t'
        s = s.decode("utf-8")
        self.assertTrue(TM.RemoveWhitespace(s)=='<td><spanclass="label">Hometown/HighSchool:</span>NewBerlin,Wis./Eisenhower</td>')

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

    def test_Narrate(self):
        TMLog_Tests.debug("\n\n-------"+TM.FnName())
        TMLog_Tests.debug(TM.Narrate(True))
        self.assertTrue("True" in TM.Narrate(True))
        TMLog_Tests.debug(TM.Narrate(False))
        self.assertTrue("False" in TM.Narrate(False))
        TMLog_Tests.debug(TM.Narrate(None))
        self.assertTrue("None" in TM.Narrate(None))
        TMLog_Tests.debug(TM.Narrate("HelloString"))
        self.assertTrue("HelloString" in TM.Narrate("HelloString"))
        vTe5tObj = Te5tObj()
        sNarration = TM.Narrate(vTe5tObj)
        TMLog_Tests.debug(sNarration)
        self.assertTrue("Name:Te5tObject" in sNarration and "Method:" in sNarration and "TypeMethod:" in sNarration)

    def test_Narrate_Elem(self):
        TMLog_Tests.debug("\n\n-------"+TM.FnName())
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vRoot = vTree.getroot()
        TMLog_Tests.debug(TM.Narrate(vRoot,iRecursionThreshold=5))
        self.assertTrue("*Tag:   	{http://schemas.microsoft.com/developer/msbuild/2003}Project" in TM.Narrate(vRoot))

    def test_Narrate_Collection(self):
        TMLog_Tests.debug("\n\n-------"+TM.FnName())
        cArray = [30,40,80,10]
        TMLog_Tests.debug(TM.Narrate(cArray))
        self.assertTrue("2:80" in TM.Narrate(cArray))

    def test_Narrate_UnknownObj(self):
        TMLog_Tests.debug("\n\n-------"+TM.FnName())
        vObj = Te5tObj()
        TMLog_Tests.debug(TM.Narrate(vObj))
        self.assertTrue("Name:Te5tObject" in TM.Narrate(vObj))

    def test_Narrate_Proj(self):
        TMLog_Tests.debug("\n\n-------"+TM.FnName())
        with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
            TMLog_Tests.debug(TM.Narrate(vProjWrapper.vProj))
            self.assertTrue("Name:HelloWorld" in TM.Narrate(vProjWrapper.vProj))


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
        print(TM.Narrate(TM.GetRelFileNames(".")))
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
    def test_openpyxl(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName()):
            vWorkbook = openpyxl.Workbook()
            vSheet = vWorkbook.active
            self.assertTrue(TM.openpyxl.IsEmptySheet(vSheet))
            self.assertEqual(0,TM.openpyxl.GetMaxCol(vSheet))
            vSheet[TM.openpyxl.PosByXY(0,0)] = "HelloWorld"
            self.assertFalse(TM.openpyxl.IsEmptySheet(vSheet))
            self.assertEqual(1,TM.openpyxl.GetMaxCol(vSheet))
            self.assertEqual("A1",TM.openpyxl.PosByCell(vSheet[TM.openpyxl.PosByXY(0,0)]))

    def test_GetNumsInString(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName()):
            cNums = TM.GetNumsInString("345.54,4ertertrt547g3r5")
            self.assertTrue(cNums == [345.54,4,547,3,5])

    def test_RunPowershellScript_Try(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            TM.RunPowerShellScript(os.path.join(os.getcwd(),'HelloWorld.ps1'))

    def test_Run(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            TM.Run("git clone -b beta https://github.com/Troy1010/TM_CommonCPP.git")

    def test_GitPullOrClone(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            TM.GitPullOrClone("https://github.com/Troy1010/TM_CommonCPP.git")

    def test_CopyExclude(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            TM.Copy("Folder2","FolderCopied",sExclude="XML")

    def test_CommandSet(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            #-Pre-checking just to be sure test is set up correctly
            print("os.getcwd():"+os.getcwd())
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            #-
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([VS.IntegrateProps,VS.IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])
            vCommandSet.Execute()
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertTrue("conanbuildinfo.props" in vHelloWorldFile.read())

    def test_CommandSet2(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
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
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
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

    def test_TryMkdir(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            self.assertFalse(os.path.isdir("Folder1a"))
            TM.TryMkdir("Folder1a")
            TM.TryMkdir("Folder1a")
            self.assertTrue(os.path.isdir("Folder1a"))

    def test_CommandSet_Save(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([VS.IntegrateProps,VS.IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])
            vCommandSet.Save()
            self.assertTrue(os.path.isfile("CommandSet.pickle"))

    def test_CommandSet_ValueError(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            vCommandSet = TM.CommandSet()
            with self.assertRaises(ValueError):
                vCommandSet.Que([VS.IntegrateProps,VS.IntegrateProps_Undo,VS.IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])

    def test_CommandSet_SingleArg(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([TM.IsCollection,TM.IsCollection],"Project.vcxproj")
            vCommandSet.Execute()

    def test_GetDependencyRoots(self):
        TMLog_Tests.debug("\n\n-------"+TM.FnName())
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            for sRoot in TM.GetDependencyRoots("conanbuildinfo.txt"):
                TMLog_Tests.debug(sRoot)

    def test_ImportFromDir(self):
        TMLog_Tests.debug("\n\n-------"+TM.FnName())
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            vModule = TM.ImportFromDir("ReturnAString.py")
            TMLog_Tests.debug(vModule.FnReturnAString())


    def test_CopyFunction(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with open("pickle1","wb") as handle:
                dill.dump(VS.IntegrateProps,handle)
            self.assertFalse(TM.IsTextInFile("vTree",'pickle1'))

            vFn = TM.CopyFunction(VS.IntegrateProps)
            with open("pickle2","wb") as handle:
                dill.dump(vFn,handle)
            self.assertTrue(TM.IsTextInFile("vTree",'pickle2'))

            with open("pickle2","rb") as handle:
                vLoadedFn = dill.load(handle)
                self.assertTrue("IntegrateProps" in TM.Narrate(vLoadedFn,bIncludePrivate=True,bIncludeProtected=True,iRecursionThreshold=2))
