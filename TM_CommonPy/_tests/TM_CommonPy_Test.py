import os
import unittest
import xml.etree.ElementTree
import openpyxl

import TM_CommonPy as TM
import VisualStudioAutomation as VS
import dill
from TM_CommonPy._tests._Logger import TMLog_LogTests
from nose.plugins.attrib import attr
from TM_CommonPy._Logger import TMLog
from TM_CommonPy._Logger2 import TMLog_TestLog
# Settings
bPostDelete = False

vCounter = TM.Counter()


class Te5tObj():
    Name = "Te5tObject"

    def Method(self):
        print("Hiii I'm the Test Object")

    def TypeMethod(self):
        print("Hiii I'm the Test Object")


class Test_TM_CommonPy_SameFolder(unittest.TestCase):
    sTestWorkspace = "_TestWorkspace_SameFolder/"

    @classmethod
    def setUpClass(self):
        self.sOldCWD = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        TM.Copy("res/Examples_Backup", self.sTestWorkspace, bPreDelete=True, bCDInto=True)

    @classmethod
    def tearDownClass(self):
        global bPostDelete
        if bPostDelete:
            os.chdir(os.path.dirname(__file__))
            TM.Delete(self.sTestWorkspace)
        os.chdir(self.sOldCWD)

    # ------Tests
    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_tk_Hello(self):
        TMLog_TestLog.debug("wooo")
        TMLog_LogTests.debug("weee")
        TMLog.debug("boop")
        TM.Hello()
        # self.assertTrue(False)

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_tk_FocusNext(self):
        vTable = TM.tk.TableFrame()
        vTable.FocusNextWritableCell()

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_Counter(self):
        vCounter_Tested = TM.Counter()
        self.assertTrue(vCounter_Tested() == 0)
        self.assertTrue(vCounter_Tested() == 1)
        self.assertTrue(vCounter_Tested() == 2)
        vCounter_Tested.reset()
        self.assertTrue(vCounter_Tested() == 0)

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GetDependencyRoots(self):
        self.assertTrue(TM.conan.GetDependencyRoots("conanbuildinfo.txt") == ["C:/Users/2troy/.conan/data/OBSEPluginDevPackage/0.1/Troy1010/channel/package/265db0df056ee777e467d81c01e1c3f405931683", "C:/Users/2troy/.conan/data/TM_CommonCPP/0.1/Troy1010/channel/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9"])

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_RemoveWhitespace(self):
        s = b'<td>\n\t\t\t\t\t\t\t\t\t<span class="label">Hometown/High School:</span>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t    \t     \t      \n    \t    \t\t    \t\t\t    \t\t\t    \t    \t\t    \t\t\t\t\t\t\t\t\tNew Berlin, Wis.\n\t\t        \t\t    \t\t\t    \t\t\t\t/\n    \t\t\t    \t\t\t    \t    \t\t    \t\t\t\t\t\t\t\t\tEisenhower\n\t\t        \t\t    \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t\t    \t\t\t\t\t    \t\t\t\t'
        s = s.decode("utf-8")
        self.assertTrue(TM.RemoveWhitespace(s) == '<td><spanclass="label">Hometown/HighSchool:</span>NewBerlin,Wis./Eisenhower</td>')

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GetScriptRoot_IsString(self):
        self.assertTrue(isinstance(TM.GetScriptRoot(), str))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GetFileContent_IsString(self):
        self.assertTrue(isinstance(TM.GetFileContent('ExampleXML.xml'), str))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GetFileContent_ByExample(self):
        self.assertEqual(TM.GetFileContent('ExampleTXT.txt'), "I am example txt.\nHear me. Or, read me, rather.")

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GetFileContent_ByExample2(self):
        self.assertTrue(TM.GetFileContent('ExampleTXT.txt') != "tyurityihghty")

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GetXMLNamespaces_ByExample(self):
        self.assertTrue(str(TM.GetXMLNamespaces('ExampleXML.xml')) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}')

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GetXMLNamespaces_ByExample_HasBOM(self):
        self.assertTrue(str(TM.GetXMLNamespaces('ExampleXML_HasBOM.xml')) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}')

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_FindElem(self):
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vElemToFind = xml.etree.ElementTree.Element("ProjectConfiguration", Include="Debug|Win32")
        vFoundElem = TM.FindElem(vElemToFind, vTree)
        self.assertTrue(vFoundElem[0].tag == "{http://schemas.microsoft.com/developer/msbuild/2003}Configuration" and vFoundElem[0].text == "Debug")
        self.assertTrue(vFoundElem[1].tag == "{http://schemas.microsoft.com/developer/msbuild/2003}Platform" and vFoundElem[1].text == "Win32")

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_FindElem_FindNothing(self):
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vElemToFind = xml.etree.ElementTree.Element("asdffdasfsdfg", Include="sfghdghrtd")
        vFoundElem = TM.FindElem(vElemToFind, vTree)
        self.assertTrue(vFoundElem is None)

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_Narrate(self):
        TMLog_LogTests.info(TM.Narrate(True))
        self.assertTrue("True" in TM.Narrate(True))
        TMLog_LogTests.info(TM.Narrate(False))
        self.assertTrue("False" in TM.Narrate(False))
        TMLog_LogTests.info(TM.Narrate(None))
        self.assertTrue("None" in TM.Narrate(None))
        TMLog_LogTests.info(TM.Narrate("HelloString"))
        self.assertTrue("HelloString" in TM.Narrate("HelloString"))
        vTe5tObj = Te5tObj()
        sNarration = TM.Narrate(vTe5tObj)
        TMLog_LogTests.info(sNarration)
        self.assertTrue("Name:Te5tObject" in sNarration and "Method:" in sNarration and "TypeMethod:" in sNarration)

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_Narrate_Elem(self):
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vRoot = vTree.getroot()
        TMLog_LogTests.info(TM.Narrate(vRoot, iRecursionThreshold=5))
        self.assertTrue("*Tag:   	{http://schemas.microsoft.com/developer/msbuild/2003}Project" in TM.Narrate(vRoot))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_Narrate_Collection(self):
        cArray = [30, 40, 80, 10]
        TMLog_LogTests.info(TM.Narrate(cArray))
        self.assertTrue("2:80" in TM.Narrate(cArray))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_Narrate_UnknownObj(self):
        vObj = Te5tObj()
        TMLog_LogTests.info(TM.Narrate(vObj))
        self.assertTrue("Name:Te5tObject" in TM.Narrate(vObj))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_Narrate_Proj(self):
        with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
            TMLog_LogTests.info(TM.Narrate(vProjWrapper.vProj))
            self.assertTrue("Name:HelloWorld" in TM.Narrate(vProjWrapper.vProj))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GetRelFileNames(self):
        TMLog_LogTests.info(TM.Narrate(TM.GetRelFileNames(".")))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_ListFiles(self):
        TMLog_LogTests.info(TM.ListFiles("."))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_IsCollection(self):
        self.assertTrue(TM.IsCollection(["beep", "boop"]))
        self.assertFalse(TM.IsCollection("beep"))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GetNumsInString(self):
        cNums = TM.GetNumsInString("345.54,4ertertrt547g3r5")
        self.assertTrue(cNums == [345.54, 4, 547, 3, 5])


class Test_TM_CommonPy(unittest.TestCase):
    sTestWorkspace = "_TestWorkspace/"

    @classmethod
    def setUpClass(self):
        self.sOldCWD = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        TM.Delete(self.sTestWorkspace)

    @classmethod
    def tearDownClass(self):
        global bPostDelete
        if bPostDelete:
            TM.Delete(self.sTestWorkspace)
        os.chdir(self.sOldCWD)

    # ------Tests
    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_COM(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                cProjFiles = TM.COM.COMCollectionToDict(vProjWrapper.vProj.Object.Files)
                TMLog_LogTests.info(TM.Narrate(cProjFiles))
                self.assertTrue(len(cProjFiles) == 4)
                for vKey, vItem in cProjFiles.items():
                    self.assertTrue(vItem.Name in ("HelloWorld.cpp", "stdafx.cpp", "stdafx.h", "targetver.h"))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_openpyxl(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName()):
            vWorkbook = openpyxl.Workbook()
            vSheet = vWorkbook.active
            self.assertTrue(TM.openpyxl.IsEmptySheet(vSheet))
            self.assertEqual(0, TM.openpyxl.GetMaxCol(vSheet))
            vSheet[TM.openpyxl.PosByXY(0, 0)] = "HelloWorld"
            self.assertFalse(TM.openpyxl.IsEmptySheet(vSheet))
            self.assertEqual(1, TM.openpyxl.GetMaxCol(vSheet))
            self.assertEqual("A1", TM.openpyxl.PosByCell(vSheet[TM.openpyxl.PosByXY(0, 0)]))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_RunPowershellScript_Try(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            self.assertFalse("IAmADir" in os.listdir())
            vProcess = TM.RunPowerShellScript(os.path.join(os.getcwd(), 'MakeDir.ps1'))
            self.assertTrue("powershell.exe" in TM.Narrate(vProcess))
            self.assertTrue("IAmADir" in os.listdir())

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_Run(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            self.assertFalse("ThisIsADir" in os.listdir())
            TM.Run("python Script_MkDir.py")
            self.assertTrue("ThisIsADir" in os.listdir())

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GitPullOrClone(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            self.assertFalse(os.path.exists("TM_CommonCPP/"))
            TM.git.PullOrClone("https://github.com/Troy1010/TM_CommonCPP.git", bQuiet=True)
            self.assertTrue(os.listdir("TM_CommonCPP/") == [".git"])

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_GitAbsoluteCheckout(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            self.assertFalse(os.path.exists("TM_CommonCPP/"))
            TM.git.AbsoluteCheckout("https://github.com/Troy1010/TM_CommonCPP.git", bQuiet=True)
            self.assertTrue(os.path.exists("TM_CommonCPP/TM_CommonCPP.sln"))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_CopyExclude(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            self.assertFalse(os.path.exists("FolderCopied/"))
            TM.Copy("Folder2", "FolderCopied", sExclude="XML")
            self.assertTrue(os.path.exists("FolderCopied/"))
            self.assertFalse(os.path.exists("FolderCopied/ExampleXML.xml"))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_CommandSet(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            # -Pre-checking just to be sure test is set up correctly
            print("os.getcwd():"+os.getcwd())
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            # -
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([VS.IntegrateProps, VS.IntegrateProps_Undo], ["HelloWorld.vcxproj", "conanbuildinfo.props"])
            vCommandSet.Execute()
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertTrue("conanbuildinfo.props" in vHelloWorldFile.read())

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_CommandSet2(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            # -Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            # -
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([VS.IntegrateProps, VS.IntegrateProps_Undo], ["HelloWorld.vcxproj", "conanbuildinfo.props"])
            vCommandSet.Execute()
            # -Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertTrue("conanbuildinfo.props" in vHelloWorldFile.read())
            # -
            vCommandSet.Execute()
            # -Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_CommandSet3(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            # ---Open
            TM.Copy("HelloWorld.vcxproj", "HelloWorld_Clean.vcxproj")
            # ---
            # -Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            # -
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([VS.IntegrateProps, VS.IntegrateProps_Undo], ["HelloWorld.vcxproj", "conanbuildinfo.props"])
            vCommandSet.Execute()
            # -Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertTrue("conanbuildinfo.props" in vHelloWorldFile.read())
            # -
            TM.Copy("HelloWorld_Clean.vcxproj", "HelloWorld.vcxproj")
            # -Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            # -
            vCommandSet.Que([VS.IntegrateProps, VS.IntegrateProps_Undo], ["HelloWorld.vcxproj", "conanbuildinfo.props"])
            vCommandSet.Execute()
            # -Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertFalse("conanbuildinfo.props" in vHelloWorldFile.read())
            # -
            vCommandSet.Que([VS.IntegrateProps, VS.IntegrateProps_Undo], ["HelloWorld.vcxproj", "conanbuildinfo.props"])
            vCommandSet.Execute(bRedo=True)
            # -Test
            with open("HelloWorld.vcxproj", 'r') as vHelloWorldFile:
                self.assertTrue("conanbuildinfo.props" in vHelloWorldFile.read())
            # -

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_TryMkdir(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            self.assertFalse(os.path.isdir("Folder1a"))
            TM.TryMkdir("Folder1a")
            TM.TryMkdir("Folder1a")
            self.assertTrue(os.path.isdir("Folder1a"))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_CommandSet_Save(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([VS.IntegrateProps, VS.IntegrateProps_Undo], ["HelloWorld.vcxproj", "conanbuildinfo.props"])
            vCommandSet.Save()
            self.assertTrue(os.path.isfile("CommandSet.pickle"))

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_CommandSet_ValueError(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            vCommandSet = TM.CommandSet()
            with self.assertRaises(ValueError):
                vCommandSet.Que([VS.IntegrateProps, VS.IntegrateProps_Undo, VS.IntegrateProps_Undo], ["HelloWorld.vcxproj", "conanbuildinfo.props"])

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_CommandSet_SingleArg_Try(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            vCommandSet = TM.CommandSet()
            vCommandSet.Que([TM.IsCollection, TM.IsCollection], "Project.vcxproj")
            vCommandSet.Execute()

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_ImportFromDir(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            vModule = TM.ImportFromDir("ReturnAString.py")
            TMLog_LogTests.info(vModule.FnReturnAString())

    @attr(**{'count': vCounter(), __name__.rsplit(".", 1)[-1]: True})
    def test_CopyFunction(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(), sSource="res/Examples_Backup", bPostDelete=False, bCDInto=True):
            with open("pickle1", "wb") as handle:
                dill.dump(VS.IntegrateProps, handle)
            self.assertFalse(TM.IsTextInFile("vTree", 'pickle1'))

            vFn = TM.CopyFunction(VS.IntegrateProps)
            with open("pickle2", "wb") as handle:
                dill.dump(vFn, handle)
            self.assertTrue(TM.IsTextInFile("vTree", 'pickle2'))

            with open("pickle2", "rb") as handle:
                vLoadedFn = dill.load(handle)
                self.assertTrue("IntegrateProps" in TM.Narrate(vLoadedFn, bIncludePrivate=True, bIncludeProtected=True, iRecursionThreshold=2))
