from unittest import TestCase
import os

import TM_CommonPy as TMCP

class Test_TM_CommonPy(TestCase):
    sExampleXMLFile = os.path.join('TM_CommonPy','tests','ExampleXML.xml')
    sExampleTXTFile = os.path.join('TM_CommonPy','tests','ExampleTXT.txt')

    def test_GetScriptRoot_IsString(self):
        s = TMCP.GetScriptRoot()
        self.assertTrue(isinstance(s, str))

    def test_GetFileContent_IsString(self):
        s = TMCP.GetFileContent(self.sExampleXMLFile)
        self.assertTrue(isinstance(s, str))

    def test_GetFileContent_ByExample(self):
        b = TMCP.GetFileContent(self.sExampleTXTFile) == "I am example txt.\nHear me. Or, read me, rather."
        self.assertTrue(b)

    def test_GetXMLNamespaces_ByExample(self):
        b = str(TMCP.GetXMLNamespaces(self.sExampleXMLFile)) == '{\'\': \'http://schemas.microsoft.com/developer/msbuild/2003\'}'
        self.assertTrue(b)
