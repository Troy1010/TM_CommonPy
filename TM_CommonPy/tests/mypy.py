import shutil, os, stat

for root, dirs, files in os.walk("Examples__Run"):
    for sFile in files:
        os.chmod(os.path.join(root,sFile), stat.S_IWRITE)

os.chmod("Examples__Run", stat.S_IWRITE)
shutil.rmtree("Examples__Run")
