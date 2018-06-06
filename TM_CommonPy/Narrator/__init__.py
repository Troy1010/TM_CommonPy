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
bDebug = False

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

#beta
def Narrate(vVar,bIncludeProtected=False,bIncludePrivate=False,bMultiLine=True,iRecursionThreshold=5):
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
    #------Pass to another Narrate command
    __self.bSentRecursionMsg = False
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
    #-COM Object
    elif str(type(vVar)) == "<class 'win32com.client.CDispatch'>":
        sReturning = Narrate_COM(vVar)
    #---Collection
    elif isinstance(vVar,(dict,list,tuple)):
        sReturning = NarrateCollection(vVar,bMultiLine)
    #---Everything else
    else:
        sReturning = NarrateObject(vVar,bIncludeProtected,bIncludePrivate)
    return sReturning

def Narrate_COM(vObj):
    s = ""
    #-Filter Depreciation Errors
    try:
        bTemp = hasattr(vObj,"Value") #This is known to throw an error for depreciated objects that do actually have Values.
    except:
        return "<DepreciationFailure>"
    #-
    if hasattr(vObj,"Count"):
        s += Narrate_COM_Collection(vObj)
    #elif hasattr(vObj,"Name") and hasattr(vObj,"Value"): #Precautionary check. This should never be true.
    #    s += " (KeyValuePair) "+str(vObj.Name) + ":" + Narrate(vObj.Value,iRecursionThreshold=__self.iRecursionThreshold)
    else:
        try:
            sItem = str(vObj)
            s += sItem
        except:
            s += "<failureToExtract>"
    return s

#If you try to vObj.Value depreciated COM objects, an error is thrown.
def GetValue_COMObject(vObj):
    try:
        bTemp = hasattr(vObj,"Value") #This is known to throw an error for depreciated objects.
    except:
        return "<ValueError>"
    return vObj.Value

def Narrate_COM_Collection(vObj):
    s = "Object_COM.."
    #---Determine bColHasKeys
    bColHasKeys = False
    for i in range(vObj.Count):
        if not hasattr(vObj[i],"Name"):
            break
    else: #If for loop never hit break.
        bColHasKeys = True
    #---
    if __self.iRecursionLvl >= __self.iRecursionThreshold:
        s += "  <RecursionLvlReached>"
    else:
        __self.iRecursionLvl += 1
        if bColHasKeys:
            for i in range(vObj.Count):
                s += __NL() + str(vObj[i].Name) + ":" + Narrate(GetValue_COMObject(vObj[i]),iRecursionThreshold=__self.iRecursionThreshold)
        else:
            for i in range(vObj.Count):
                s += __NL() + str(i)+":"+Narrate(vObj[i],iRecursionThreshold=__self.iRecursionThreshold)
        __self.iRecursionLvl -= 1
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
        s += "  <RecursionLvlReached>"
    else:
        __self.iRecursionLvl += 1
        for vKey,vValue in cExtrasBeingNarrated.items():
            sReturning += __NL() + vKey + ":" + vValue
        for sProperty in cPropertiesBeingNarrated:
            sReturning += __NL() + sProperty + ":" + Narrate(getattr(vObj, sProperty),iRecursionThreshold=__self.iRecursionThreshold)
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
        if __self.iRecursionLvl >= __self.iRecursionThreshold:
            s += "  <RecursionLvlReached>"
        else:
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
            sReturning += Narrate(vValue,iRecursionThreshold=__self.iRecursionThreshold)
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
            sReturning += ":" + Narrate(vValue,iRecursionThreshold=__self.iRecursionThreshold)
            __self.iRecursionLvl -= 1
        sReturning += "}"
        return sReturning
