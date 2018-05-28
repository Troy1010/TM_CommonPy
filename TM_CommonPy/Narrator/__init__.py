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
sIndent = " "
iRecursionLvl = 0
iRecursionThreshold = 5
bSentRecursionMsg = False

def __Indent():
    return __self.sIndent * __self.iRecursionLvl

#Indented NewLine
def __NL():
    return "\n" +__Indent()

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
def Narrate(vVar,bIncludeProtected=False,bIncludePrivate=False,bMultiLine=True,iRecursionThreshold=5):
    #------Handle Recursion
    __self.iRecursionThreshold = iRecursionThreshold
    if __self.iRecursionLvl > __self.iRecursionThreshold:
        if not bSentRecursionMsg:
            bSentRecursionMsg = True
            sReturning = "<ReachedRecursionThreshold>"
        else:
            sReturning = ""
    #------Pass to another Narrate command
    else:
        bSentRecursionMsg = False
        #---If it's a simple variable, return it as a string.
        if isinstance(vVar,(str,numbers.Number)):   #This also captures bools.
            sReturning = str(vVar)
        #---None
        elif vVar is None:
            sReturning = "<None>"
        #---Known Objects
        #-etree Element
        elif isinstance(vVar,xml.etree.ElementTree.Element):
            sReturning = NarrateElem(vVar)
        #---Collection
        elif isinstance(vVar,(dict,list,tuple)):
            sReturning = NarrateCollection(vVar,bMultiLine)
        #---Everything else
        else:
            sReturning = NarrateObject(vVar,bIncludeProtected,bIncludePrivate)
    return sReturning

#cMembers are exclusionary if they start full, inclusionary if they start empty.
def NarrateObject(vObj,bIncludeProtected=False,bIncludePrivate=False, cMembers=[], bStartFull=True):
    return NarrateObject_Options(vObj, bIncludeProtected, bIncludePrivate, cMembers, cMembers, cMembers, bStartFull, bStartFull, bStartFull)

#cMethods, cProperties, cExtras are exclusionary if they start full, inclusionary if they start empty.
def NarrateObject_Options(vObj,bIncludeProtected=False,bIncludePrivate=False, cMethods = [], cProperties = [], cExtras = [], bMethodsStartFull = True, bPropertiesStartFull = True, bExtrasStartFull = True):
    sReturning = ""
    #------Reflection
    #---Reflect the object's members
    if not bIncludeProtected:
        cMembers = [x for x in dir(vObj) if not x.startswith("_")]
    elif not bIncludePrivate:
        cMembers = [x for x in dir(vObj) if not x.startswith("__")]
    else:
        cMembers = dir(vObj)
    #---Seperate cMethodsBeingNarrated and cPropertiesBeingNarrated from cMembers. Define cExtrasBeingNarrated.
    cExtrasBeingNarrated = {"Type":str(type(vObj))}
    cPropertiesBeingNarrated = [a for a in cMembers if not callable(getattr(vObj, a))]
    cMethodsBeingNarrated = [a for a in cMembers if callable(getattr(vObj, a))]
    #---Empty
    if len(cPropertiesBeingNarrated) ==0 and len(cMethodsBeingNarrated) ==0:
        sReturning += "<EmptyObject>"
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
    __self.iRecursionLvl += 1
    for vKey,vValue in cExtrasBeingNarrated.items():
        sReturning += __NL() + vKey + ":" + vValue
    for sProperty in cPropertiesBeingNarrated:
        sReturning += __NL() + sProperty + ":" + Narrate(getattr(vObj, sProperty))
    for sMethod in cMethodsBeingNarrated:
        sReturning += __NL() + sMethod + ":" + "Method"
    __self.iRecursionLvl -= 1
    #---small fixes
    if sReturning == "":
        sReturning += "<Object>"
    else:
        sReturning = "Object.." + sReturning
    return sReturning

#Warning, this function may hang
#def NarrateUnknown(vVar, cAttributes = None):
#    sReturning = "*Type:" + str(type(vVar))
#    if hasattr(vVar,'Name'):
#        sReturning += __NL() + "Name:"+vVar.Name
#    try:
#        for sAttrib in cAttributes:
#            try:
#                sReturning += __NL() + sAttrib + ":" + Narrate(getattr(vVar,sAttrib))
#            except:
#                pass
#    except:
#        pass
#    if __IsIterable(vVar):
#        sReturning += __NL() + "children.."
#        __self.iIndent += 1
#        for vChild in vVar:
#            sReturning += __NL() + Narrate(vChild)
#        __self.iIndent -= 1
#    return sReturning

#beta
def NarrateElem(vElem):
    sReturning = "*Tag:   \t"+str(vElem.tag)
    if not (vElem.text is None or vElem.text.isspace()):
        sReturning += __NL()+"text:  \t"+str(vElem.text).replace("\n","\\n")
    if not TMC.IsEmpty(vElem.attrib):
        sReturning += __NL()+"attrib:\t"+NarrateCollection(vElem.attrib, bMultiLine=False)
    if len(list(vElem)) !=0:
        sReturning += __NL()+"children.."
        __self.iRecursionLvl += 1
        for vChild in vElem:
            sReturning += __NL() + NarrateElem(vChild)
        __self.iRecursionLvl -= 1
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
        __self.iRecursionLvl += 1
        for vKey,vValue in cCollection:
            sReturning += __NL() + str(vKey) + ":"
            sReturning += Narrate(vValue)
        __self.iRecursionLvl -= 1
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
            __self.iRecursionLvl += 1
            sReturning += ":" + Narrate(vValue)
            __self.iRecursionLvl -= 1
        sReturning += "}"
        return sReturning
