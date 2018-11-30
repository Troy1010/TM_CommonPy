import xml.etree.ElementTree
import TM_CommonPy as TM

class ElementTreeContext:
    def __init__(self,sXMLFile,bSave=True):
        self.bSave = bSave
        self.sXMLFile = sXMLFile
        self.vTree = xml.etree.ElementTree.parse(self.sXMLFile)
    def __enter__(self):
        return self.vTree
    def __exit__(self,errtype,value,traceback):
        if self.bSave:
            #-Register namespaces, otherwise ElementTree will prepend all elements with the namespace.
            for sKey, vValue in TM.GetXMLNamespaces(self.sXMLFile).items():
                xml.etree.ElementTree.register_namespace(sKey, vValue)
            self.vTree.write(self.sXMLFile)
