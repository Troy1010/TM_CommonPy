import os
import TM_CommonPy as TM

#dev
def GetGitTitleFromURL(sURL):
    return sURL[sURL.rfind("/")+1:sURL.rfind(".git")]

#dev
def PullOrClone(sURL,bCDInto=False,bQuiet=False):
    #---Open
    sCWD = os.getcwd()
    sName = GetGitTitleFromURL(sURL)
    #---
    #-Try to find .git
    sPathToGit = ""
    if os.path.exists(".git"):
        sPathToGit = "."
    elif os.path.exists(os.path.join(sName,".git")):
        sPathToGit = sName
    #-Pull or clone
    if sPathToGit != "":
        os.chdir(sPathToGit)
        sRunCmd = "git pull "+sURL
        if bCDInto:
            sCWD = "."
    else:
        sRunCmd = "git clone "+sURL+" --no-checkout"
        if bCDInto:
            sCWD = sName
    if bQuiet:
        sRunCmd += " --quiet"
    TM.Run(sRunCmd)
    #---Close
    os.chdir(sCWD)

#dev
def FullClean(bStash = False, bQuiet=False):
    if bStash:
        if bQuiet:
            TM.Run("git stash -u --quiet")
        else:
            TM.Run("git stash -u")
    else:
        if bQuiet:
            TM.Run("git clean -f --quiet")
            TM.Run("git reset --hard --quiet")
        else:
            TM.Run("git clean -f")
            TM.Run("git reset --hard")

#dev
def AbsoluteCheckout(sURL,sBranch="",bQuiet=False):
    #---Open
    sCWD = os.getcwd()
    sName = GetGitTitleFromURL(sURL)
    #---Get .git
    PullOrClone(sURL,bCDInto=True,bQuiet=bQuiet)
    #---Clean
    FullClean(bQuiet=bQuiet)
    #---Checkout
    if bQuiet:
        TM.Run("git checkout "+sBranch+" --quiet")
    else:
        TM.Run("git checkout "+sBranch)
    #---Close
    os.chdir(sCWD)
