from unittest import TestCase
import os
import shutil
import sys


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

    def test_Copy_ByExample(self):
        TMC.Copy('Examples','Examples_TmpCopy')
        b = False
        if os.path.isfile(os.path.join('Examples_TmpCopy','ExampleXML.xml')) and os.path.isfile(os.path.join('Examples_TmpCopy','ExampleTXT.txt')):
            b = True
        shutil.rmtree('Examples_TmpCopy')
        self.assertTrue(b)
