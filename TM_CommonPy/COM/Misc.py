
def COMCollectionToDict(cCOMCollection, bTry=True):
    cReturning = {}
    if bTry and cCOMCollection is None:
        return cReturning
    #-Determine bCollectionOfPairs
    #Checking for Value is tricky because hasattr will throw an error for depreciated objects
    bCollectionOfPairs = False
    for i in range(cCOMCollection.Count):
        try:
            if not hasattr(cCOMCollection[i],"Value"): #This is known to throw an error for depreciated objects.
                break
        except:
            pass
    else:
        bCollectionOfPairs = True
    #-
    for i in range(cCOMCollection.Count):
        if bCollectionOfPairs:
            cReturning[cCOMCollection[i].Name] = TryGetValue(cCOMCollection[i])
        else:
            cReturning[i] = cCOMCollection[i]
    return cReturning

def TryGetValue(vObj):
    try:
        if hasattr(vObj,"Value"): #This is known to throw an error for depreciated objects.
            return getattr(vObj,"Value")
        return "<None>"
    except:
        return "<ValueError>"
