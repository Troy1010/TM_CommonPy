import TM_CommonPy as TM
import VisualStudioAutomation as VS
from pprint import pprint

def test(sStr):
    if iter(sStr) and not isinstance(sStr,str):
        print("True")
    else:
        print("False")
        pass

test(["good"])
