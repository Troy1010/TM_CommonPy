import unittest
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree

import TM_CommonPy as TMC
import TM_CommonPy.Narrator as TMC_NAR

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

    def TestMethod(self):
        print("Hiii I'm the Test Object")

    def TypeMethod(self):
        print("Hiii I'm the Test Object")


class Test_TM_CommonPy(unittest.TestCase):

    sExampleXMLFile = 'ExampleXML.xml'
    sExampleXML_HasBOM = 'ExampleXML_HasBOM.xml'
    sExampleTXTFile = 'ExampleTXT.txt'

    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('TM_CommonPy','tests'))

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        TMC.Copy('Examples_Backup','Examples')
        os.chdir('Examples')

    def tearDown(self):
        os.chdir('..')
        shutil.rmtree('Examples')

    #------Tests

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
        b = TMC.GetFileContent(self.sExampleTXTFile) == "tyurityihghty"
        self.assertTrue(not b)

    def test_GetXMLNamespaces_ByExample(self):
        b = str(TMC.GetXMLNamespaces(self.sExampleXMLFile)) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}'
        self.assertTrue(b)

    def test_GetXMLNamespaces_ByExample_HasBOM(self):
        b = str(TMC.GetXMLNamespaces(self.sExampleXML_HasBOM)) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}'
        self.assertTrue(b)

    def test_Copy_ByExample(self):
        b = False
        if os.path.isfile('ExampleXML.xml') and os.path.isfile('ExampleTXT.txt'):
            b = True
        self.assertTrue(b)

    def test_FindElem(self):
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vElemToFind = xml.etree.ElementTree.Element("ProjectConfiguration", Include="Debug|Win32")
        vFoundElem = TMC.FindElem(vElemToFind,vTree)
        self.assertTrue(vFoundElem[0].tag == "{http://schemas.microsoft.com/developer/msbuild/2003}Configuration" and vFoundElem[0].text == "Debug")
        self.assertTrue(vFoundElem[1].tag == "{http://schemas.microsoft.com/developer/msbuild/2003}Platform" and vFoundElem[1].text == "Win32")

    def test_FindElem_FindNothing(self):
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vElemToFind = xml.etree.ElementTree.Element("asdffdasfsdfg", Include="sfghdghrtd")
        vFoundElem = TMC.FindElem(vElemToFind,vTree)
        self.assertTrue(vFoundElem is None)

    def test_Narrate_Elem(self):
        vTree = xml.etree.ElementTree.parse('ExampleXML.xml')
        vRoot = vTree.getroot()
        print(TMC_NAR.Narrate(vRoot))
        #self.assertTrue(False)

    def test_Narrate_Collection(self):
        cArray = [30,40,80,10]
        print(TMC_NAR.Narrate(cArray))
        #self.assertTrue(False)

    def test_Narrate_Bool(self):
        print(TMC_NAR.Narrate(True))
        print(TMC_NAR.Narrate(False))
        #self.assertTrue(False)

    def test_Narrate_None(self):
        print(TMC_NAR.Narrate(None))
        #self.assertTrue(False)

    def test_Narrate_UnknownObj(self):
        vObj = TestObj()
        print(TMC_NAR.Narrate(vObj))
        #self.assertTrue(False)

    def test_Narrate_Object2(self):
        vObj = TestObj()
        print(TMC_NAR.NarrateObject(vObj))
        print("========")
        print(TMC_NAR.NarrateObject_Options(vObj, bMethodsStartFull=False, bExtrasStartFull=False))
        #self.assertTrue(False)

    def test_Copy(self):
        os.chdir('..')
        TMC.Copy('Examples_Backup','Examples_Copy',bPreDelete=True)
        os.chdir('Examples_Copy')

    #---GetDictCount
    def test_GetDictCount_ByExample(self):
        cDict = {"age":25,"blue":3,"cat":5}
        self.assertTrue(TMC.GetDictCount(cDict) == 3)

    def test_RunPowershellScript_Try(self):
        print(os.path.join(os.getcwd(),'HelloWorld.ps1'))
        TMC.RunPowerShellScript(os.path.join(os.getcwd(),'HelloWorld.ps1'))
        #TMC.RunPowershellScript('HelloWorld.ps1')
        #self.assertTrue(False)

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


    #def test_RunPowershellScript_Try(self):
    #    #---Open
    #    TMC.Copy('Examples','Examples_RunPowershellScript_Try')
    #    #---
    #    TMC.RunPowershellScript(os.path.join(os.getcwd(),'Examples_RunPowershellScript_Try','HelloWorld.ps1'))
    #    self.assertTrue(False)
    #    #---Close
    #    shutil.rmtree('Examples_NarrateElem')


#    def test_WhatIsThisTrueFalse(self):
#        #---Open
#        TMC.Copy('Examples','Examples_WhatIsThisTrueFalse')
#        #---
#        vTree = xml.etree.ElementTree.parse(os.path.join('Examples_WhatIsThisTrueFalse','ExampleXML.xml'))
#        for vElem in vTree.iter():
#            print("vElem.tag:"+str(vElem.tag))
#            print("vElem.text:"+str(vElem.text))
#        self.assertTrue(False)
#        #---Close
#        shutil.rmtree('Examples_WhatIsThisTrueFalse')
