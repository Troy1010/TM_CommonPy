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
bDebug = False




def __Indent():
    return __self.sIndent * __self.iRecursionLvl

#Indented NewLine
def __NL():
    return "\n" +__Indent()

class RecursionContext:
    def __init__(self,s):
        self.s = s
    def __enter__(self):
        global iRecursionLvl
        iRecursionLvl += 1
        return self.s + " bob"
    def __exit__(self, type, value, traceback):
        global iRecursionLvl
        iRecursionLvl -= 1

def test():
    s = "hey"
    with RecursionContext(s) as s:
        pass
    print(s)


#------Public
#master
def Print(sPrintMe):
    print(sPrintMe)

#beta
#I didn't bump recursion lvl as param because it wouldn't affect __NL()
def Narrate(vVar,bIncludeProtected=False,bIncludePrivate=False,bMultiLine=True,iRecursionThreshold=5,cMembers=[],bStartFull=True):
    #------Handle Recursion
    #Recursion should be checked before Narrate is called. This re-check is just a precaution.
    if bDebug:
        print("__self.iRecursionThreshold:"+str(__self.iRecursionThreshold)+" __self.iRecursionLvl:"+str(__self.iRecursionLvl))
    __self.iRecursionThreshold = iRecursionThreshold
    if __self.iRecursionLvl > __self.iRecursionThreshold: #If =, we're on the last lvl.
        if not __self.bSentRecursionMsg:
            __self.bSentRecursionMsg = True
            if bDebug:
                print("HitRecursionThreshold")
            return "<ReachedRecursionThreshold>"
        else:
            return ""
    __self.bSentRecursionMsg = False
    #------Pass to another Narrate command
    #-COM Object
    if str(type(vVar)) == "<class 'win32com.client.CDispatch'>":
        sReturning = Narrate_COM(vVar)
    #---If it's a simple variable, return it as a string.
    elif isinstance(vVar,(str,numbers.Number)):   #This also captures bools.
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
        sReturning = NarrateObject(vVar,bIncludeProtected,bIncludePrivate,cMembers,bStartFull)
    return sReturning

def Narrate_COM(vObj):
    s = ""
    #-
    if hasattr(vObj,"Count"):
        s += Narrate_COM_Collection(vObj)
    elif hasattr(vObj,"Name"):
        s += Narrate_COM_Object(vObj)
    else:
        try:
            sItem = str(vObj)
            s += sItem
        except:
            s += "<failureToExtract>"
    return s

#If you try to vObj.Value depreciated COM objects, an error is thrown.
def GetValueOfPair_COMObject(vObj):
    try:
        if hasattr(vObj,"Value"): #This is known to throw an error for depreciated objects.
            return getattr(vObj,"Value")
        else:
            return "<None>"
    except:
        return "<ValueError>"

#dir() does not work for all members of COM objects
def GetMembers_COM(vObj,cPossibleKeys=[]):
    if not cPossibleKeys:
        cPossibleKeys = ["Name"
            ,"Object"
            ,"Collection"
            ,"ProjectItems"
            ,"Properties"]
    cMembers = {}
    for vKey in cPossibleKeys:
        if hasattr(vObj,vKey):
            vValue = getattr(vObj,vKey)
            cMembers[vKey] = vValue
    return cMembers.items()

def Narrate_COM_Object(vObj,cPossibleKeys=[],iRecursionThreshold=-1):
    if iRecursionThreshold != -1:
        __self.iRecursionThreshold = iRecursionThreshold
    s = "Object_COM.."
    #---
    if __self.iRecursionLvl >= __self.iRecursionThreshold:
        s += "  <RecursionLvlReached>"
    else:
        with RecursionContext():
            for vKey,vValue in GetMembers_COM(vObj,cPossibleKeys):
                s += __NL() + vKey + ":" + Narrate(vValue,iRecursionThreshold=__self.iRecursionThreshold)
    return s


def Narrate_COM_Collection(cCollection):
    s = "Collection_COM.."
    #---Determine bColHasKeys
    bColHasKeys = False
    for i in range(cCollection.Count):
        if not hasattr(cCollection[i],"Name"):
            break
    else: #If for loop never hit break.
        bColHasKeys = True
    #---
    if __self.iRecursionLvl >= __self.iRecursionThreshold:
        s += "  <RecursionLvlReached>"
    else:
        with RecursionContext():
            if bColHasKeys:
                for i in range(cCollection.Count):
                    s += __NL() + str(cCollection[i].Name) + ":" + Narrate(GetValueOfPair_COMObject(cCollection[i]),iRecursionThreshold=__self.iRecursionThreshold)
            else:
                for i in range(cCollection.Count):
                    s += __NL() + str(i)+":"+Narrate(cCollection[i],iRecursionThreshold=__self.iRecursionThreshold)
    return s



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
    if __self.iRecursionLvl >= __self.iRecursionThreshold:
        sReturning += "  <RecursionLvlReached>"
    else:
        with RecursionContext():
            for vKey,vValue in cExtrasBeingNarrated.items():
                sReturning += __NL() + vKey + ":" + vValue
            for sProperty in cPropertiesBeingNarrated:
                sReturning += __NL() + sProperty + ":" + Narrate(getattr(vObj, sProperty),iRecursionThreshold=__self.iRecursionThreshold)
            for sMethod in cMethodsBeingNarrated:
                sReturning += __NL() + sMethod + ":" + "Method"
    #---small fixes
    if sReturning == "":
        sReturning += "<Object>"
    else:
        sReturning = "Object.." + sReturning
    return sReturning

#beta
def NarrateElem(vElem):
    sReturning = "*Tag:   \t"+str(vElem.tag)
    if not (vElem.text is None or vElem.text.isspace()):
        sReturning += __NL()+"text:  \t"+str(vElem.text).replace("\n","\\n")
    if not TMC.IsEmpty(vElem.attrib):
        sReturning += __NL()+"attrib:\t"+NarrateCollection(vElem.attrib, bMultiLine=False)
    if len(list(vElem)) !=0:
        sReturning += __NL()+"children.."
        if __self.iRecursionLvl >= __self.iRecursionThreshold:
            sReturning += "  <RecursionLvlReached>"
        else:
            with RecursionContext():
                for vChild in vElem:
                    sReturning += __NL() + NarrateElem(vChild)
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
        sReturning = "Collection.."
        if __self.iRecursionLvl >= __self.iRecursionThreshold:
            sReturning += "  <RecursionLvlReached>"
        else:
            with RecursionContext():
                for vKey,vValue in cCollection:
                    sReturning += __NL() + str(vKey) + ":"
                    sReturning += Narrate(vValue,iRecursionThreshold=__self.iRecursionThreshold)
        return sReturning
    else:
        sReturning = "{"
        bDoOnce = False
        if __self.iRecursionLvl >= __self.iRecursionThreshold:
            sReturning += "  <RecursionLvlReached>"
        else:
            with RecursionContext():
                for vKey,vValue in cCollection:
                    if not bDoOnce:
                        bDoOnce = True
                    else:
                        sReturning += " , "
                    sReturning += str(vKey)
                    sReturning += ":" + Narrate(vValue,iRecursionThreshold=__self.iRecursionThreshold)
        sReturning += "}"
        return sReturning
