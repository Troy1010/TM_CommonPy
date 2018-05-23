#In python, this file is already considered a class
import os, sys
import importlib
import pip
import xml.etree.ElementTree
import shutil
import TM_CommonPy as TMC

self_module = sys.modules[__name__]
iIndent = 0
sIndent = "-"

def __Indent():
    return self_module.sIndent * self_module.iIndent

#Indented NewLine
def __NL():
    return "\n"+__Indent()

#------Public

#beta
def NarrateElem(vElem):
    sReturning = __Indent() +"Tag:   \t"+str(vElem.tag)
    if not (vElem.text is None or vElem.text.isspace()):
        sReturning += __NL()+"text:  \t"+str(vElem.text).replace("\n","\\n")
    if not TMC.IsEmpty(vElem.attrib):
        sReturning += __NL()+"attrib:\t"+NarrateCollection(vElem.attrib)
    if len(list(vElem)) !=0:
        sReturning += __NL()+"children.."
        self_module.iIndent += 1
        for vChild in vElem:
            sReturning += "\n" + NarrateElem(vChild)
        self_module.iIndent -= 1
    return sReturning

#beta
#does not yet support bMultiLine
def NarrateCollection(cCollection,bMultiLine = False):
    #---None
    if cCollection is None:
        return "<None>"
    #---Dict
    if isinstance(cCollection,dict):
        cCollection = cCollection.items()
    #---NotACollection
    try:
        for vKey,vValue in cCollection:
            pass
    except:
        return "<NotACollection>"
    #---Empty
    if len(cCollection) ==0:
        return "<EmptyCollection>"
    #---
    if bMultiLine:
        raise "NarrateCollection|Does not yet support bMultiLine"
    else:
        sReturning = "{"
        bDoOnce = False
        for vKey,vValue in cCollection:
            if not bDoOnce:
                bDoOnce = True
            else:
                sReturning += " , "
            sReturning += str(vKey) + ":" + str(vValue)
        sReturning += "}"
        return sReturning
