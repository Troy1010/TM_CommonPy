import subprocess
import TM_CommonPy as TM
import sys
# Settings
bPause = False


def RunTests(sTestPath=".", sEval="True", iVerbosity=1, bPause=False):
    try:
        subprocess.run(['python', 'setup.py', 'nosetests', '--tests',
                        sTestPath, '--stop', '--verbosity='+str(iVerbosity),
                        '--eval-attr', sEval])
    except Exception as e:
        TM.DisplayException(e)
        sys.exit(1)
    if bPause:
        TM.DisplayDone()


def UploadToPyPI(bPause=False):
    try:
        TM.Delete("build")
        TM.Delete("dist")
        TM.Run("python setup.py sdist bdist_wheel")
        TM.Run("twine upload dist/*")
    except Exception as e:
        TM.DisplayException(e)
        sys.exit(1)
    if bPause:
        TM.DisplayDone()
