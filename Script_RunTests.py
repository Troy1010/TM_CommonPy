##region Settings
bPause = True
##endregion

import TM_CommonPy as TM
import os

try:
    TM.Run("python setup.py nosetests --tests=TM_CommonPy._tests --stop --verbosity=1")
except Exception as e:
    print(e)
    os.system('pause')
    raise
if bPause:
    print("\n\t\t\tDone\n")
    os.system('pause')
