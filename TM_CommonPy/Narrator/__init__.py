#In python, this file is already considered a class
import os, sys
import importlib
import pip
import xml.etree.ElementTree
import shutil
import TM_CommonPy as TMC
import collections
import numbers

__self = sys.modules[__name__]
iIndent = 0
sIndent = "-"
iRecursionLvl = 0
iRecursionThreshold = 5
bSentRecursionMsg = False

def __Indent():
    return __self.sIndent * __self.iIndent

#Indented NewLine
def __NL():
    return "\n"+__Indent()

def __IsIterable(vVar):
    try:
        #_ = (e for e in vVar)
        for vChild in vVar:
            pass
        return True
    except:
        return False

#------Public

#dev
def Narrate(vVar, bMultiLine = True):
    #------Handle Recursion
    __self.iRecursionLvl += 1
    if __self.iRecursionLvl > iRecursionThreshold:
        if not bSentRecursionMsg:
            bSentRecursionMsg = True
            __self.iRecursionLvl -= 1
            return "<ReachedRecursionThreshold>"
        else:
            __self.iRecursionLvl -= 1
            return ""
    else:
        bSentRecursionMsg = False
    #------Pass to correct Narrate command
    #---If it's a simple variable, return it as a string.
    if isinstance(vVar,(str,numbers.Number)):   #This also captures bools.
        __self.iRecursionLvl -= 1
        return str(vVar)
    #---None
    if vVar is None:
        __self.iRecursionLvl -= 1
        return "<None>"
    #---Known Objects
    #-etree Element
    if isinstance(vVar,xml.etree.ElementTree.Element):
        sReturning = NarrateElem(vVar)
        __self.iRecursionLvl -= 1
        return sReturning
    #---Collection
    if isinstance(vVar,(dict,list,tuple)):
        sReturning = NarrateCollection(vVar,bMultiLine)
        __self.iRecursionLvl -= 1
        return sReturning
    #---Everything else
    sReturning = NarrateObject(vVar)
    __self.iRecursionLvl -= 1
    return sReturning

#cMembers are exclusionary if they start full, inclusionary if they start empty.
def NarrateObject(vObj, bIncludePrivate=False, cMembers=[], bStartFull=True):
    return NarrateObject_Options(vObj, bIncludePrivate, cMembers, cMembers, cMembers, bStartFull, bStartFull, bStartFull)

#cMethods, cProperties, cExtras are exclusionary if they start full, inclusionary if they start empty.
def NarrateObject_Options(vObj, bIncludePrivate = False, cMethods = [], cProperties = [], cExtras = [], bMethodsStartFull = True, bPropertiesStartFull = True, bExtrasStartFull = True):
    #------Reflection
    #---Reflect the object's members
    if not bIncludePrivate:
        cMembers = [x for x in dir(vObj) if not "__" in x]
    else:
        cMembers = dir(vObj)
    #---Seperate cMethodsBeingNarrated and cPropertiesBeingNarrated from cMembers. Define cExtrasBeingNarrated.
    cExtrasBeingNarrated = {"Type":str(type(vObj))}
    cPropertiesBeingNarrated = [a for a in cMembers if not callable(getattr(vObj, a))]
    cMethodsBeingNarrated = [a for a in cMembers if callable(getattr(vObj, a))]
    #------Exclusion/Inclusion
    if bExtrasStartFull:
        cExtrasBeingNarrated = { k : cExtrasBeingNarrated[k] for k in set(cExtrasBeingNarrated) - set(cExtras) }
    else:
        cExtrasBeingNarrated = { k : cExtrasBeingNarrated[k] for k in set(cExtrasBeingNarrated) & set(cExtras) }
    if bPropertiesStartFull:
        cPropertiesBeingNarrated = [a for a in cPropertiesBeingNarrated if a not in cProperties]
    else:
        cPropertiesBeingNarrated = [a for a in cPropertiesBeingNarrated if a in cProperties]
    if bMethodsStartFull:
        cMethodsBeingNarrated = [a for a in cMethodsBeingNarrated if a not in cMethods]
    else:
        cMethodsBeingNarrated = [a for a in cMethodsBeingNarrated if a in cMethods]
    #------Narration
    sReturning = ""
    for vKey,vValue in cExtrasBeingNarrated.items():
        sReturning += __NL() + vKey + ":" + vValue
    for sProperty in cPropertiesBeingNarrated:
        sReturning += __NL() + sProperty + ":" + Narrate(getattr(vObj, sProperty))
    for sMethod in cMethodsBeingNarrated:
        sReturning += __NL() + "Method:" + sMethod
    #---small fixes
    if sReturning == "":
        return "<EmptyObject>"
    else:
        sReturning = "*" + sReturning.replace("\n","",1)
    return sReturning

#Warning, this function may hang
def NarrateUnknown(vVar, cAttributes = None):
    sReturning = "*Type:" + str(type(vVar))
    if hasattr(vVar,'Name'):
        sReturning += __NL() + "Name:"+vVar.Name
    try:
        for sAttrib in cAttributes:
            try:
                sReturning += __NL() + sAttrib + ":" + Narrate(getattr(vVar,sAttrib))
            except:
                pass
    except:
        pass
    if __IsIterable(vVar):
        sReturning += __NL() + "children.."
        __self.iIndent += 1
        for vChild in vVar:
            sReturning += __NL() + Narrate(vChild)
        __self.iIndent -= 1
    return sReturning

#beta
def NarrateElem(vElem):
    sReturning = "*Tag:   \t"+str(vElem.tag)
    if not (vElem.text is None or vElem.text.isspace()):
        sReturning += __NL()+"text:  \t"+str(vElem.text).replace("\n","\\n")
    if not TMC.IsEmpty(vElem.attrib):
        sReturning += __NL()+"attrib:\t"+NarrateCollection(vElem.attrib, False)
    if len(list(vElem)) !=0:
        sReturning += __NL()+"children.."
        __self.iIndent += 1
        for vChild in vElem:
            sReturning += __NL() + NarrateElem(vChild)
        __self.iIndent -= 1
    return sReturning

#beta
def NarrateCollection(cCollection,bMultiLine = True):
    #------Convert to 2xiter collection
    #---Dict
    if isinstance(cCollection,dict):
        cCollection = cCollection.items()
    #---
    try:
        for vKey,vValue in cCollection:
            pass
    except:
        try:
            cTemp = {}
            i=0
            for vValue in cCollection:
                cTemp[str(i)] = vValue
                i += 1
            cCollection = cTemp.items()
        except:
            return "<Unknown>"
    #---Empty
    if len(cCollection) ==0:
        return "<EmptyCollection>"
    #------Narrate the collection.
    if bMultiLine:
        sReturning = "*Collection.."
        __self.iIndent += 1
        for vKey,vValue in cCollection:
            sReturning += __NL() + str(vKey) + ":"
            sReturning += Narrate(vValue)
        __self.iIndent -= 1
        return sReturning
    else:
        sReturning = "{"
        bDoOnce = False
        for vKey,vValue in cCollection:
            if not bDoOnce:
                bDoOnce = True
            else:
                sReturning += " , "
            sReturning += str(vKey)
            sReturning += ":" + Narrate(vValue)
        sReturning += "}"
        return sReturning
