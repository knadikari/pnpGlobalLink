import os

import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)


from DB.DataBase import SQLDB
import subprocess


db=SQLDB()

def ExecutePythonScript():
    fullpath=os.environ['HOME']+"/pnpprg" + "/a.py"
    if(os.path.exists(fullpath)):
        process = subprocess.Popen(['python', fullpath])
        process.wait()
    else:
        print "No program found"



db.setStatus(False)


ExecutePythonScript()

db.setStatus(True)

