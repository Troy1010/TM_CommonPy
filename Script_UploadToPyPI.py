##region Settings
bPause = True
##endregion

import TM_CommonPy as TM
import os

try:
    TM.Delete("build")
    TM.Delete("dist")
    TM.Run("python setup.py sdist bdist_wheel")
    TM.Run("twine upload dist/*")
except Exception as e:
    print(e)
    os.system('pause')
    raise
if bPause:
    print("\n\t\t\tDone\n")
    os.system('pause')
