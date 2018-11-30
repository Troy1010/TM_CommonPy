##region Settings
bPause = False
##endregion

import os
import subprocess

try:
    sEvalExr = '(count < 13 and TM_CommonPy_Test)'
    subprocess.run(['python','setup.py','nosetests','--tests','TM_CommonPy._tests','--stop','--verbosity=1','--eval-attr',sEvalExr])
except Exception as e:
    print(e)
    os.system('pause')
    raise
if bPause:
    print("\n\t\t\tDone\n")
    os.system('pause')
