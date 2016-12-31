# import os
#
# try:
#     path = "/tmp/my_program.fifo"
#     os.mkfifo(path)
# except:
#     print "A"
#
# path = "/tmp/my_program.fifo"
# while True:
#     fifo = open(path, "r")
#     print fifo.read()
#     fifo.close()


import json
import os
import subprocess

import time
from initdb import initdbclass
from ControlHandler import ControlHandler

def processCleanUp(procname):
    tmp = os.popen("ps aux").read()
    pslist=[]
    #print tmp
    for line in tmp.split("\n"):
        x=1
        line=line.strip()
        procdata=line.split(" ")
        for c in range(0,procdata.count('')):
            procdata.remove('')
        #print procdata
        try:
            if(procname in procdata[11]):
                try:
                    pslist.append(int(procdata[1]))
                except Exception as e:
                    pass
                    #print "Error occured in init process cleanup:- "+e.message
        except Exception as e:
            pass
            #print "Error occured in init process cleanup Main try :- "+e.message
    #print pslist
    for p in pslist:
        try:
            if(os.getpid()!=p):
                print p,os.getpid()
                os.kill(p,9)
        except Exception as e:
            print "Error occured in init process cleanup (Killing):- " + e.message


processCleanUp("inputDeamon.py")
processCleanUp("outputdeamon.py")

path = "/tmp/control"
try:
    os.mkfifo(path)
except Exception as e:
    pass
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

proccontrol = subprocess.Popen(['python', dir_path+'/newDeamon.py'])
procinput = subprocess.Popen(['python', dir_path+'/inputdeamon/inputDeamon.py'])
procoutput = subprocess.Popen(['python', dir_path+'/outputdeamon/outputdeamon.py'])
process = subprocess.Popen(['python', os.environ['HOME']+"/a.py"])

def getFromControl():
    fifo = open(path, "r")
    msg=fifo.read()
    jobj=json.loads(msg)
    db=initdbclass()
    id=db.getdata("processname")
    print id
    mysettings=jobj[id]
    return mysettings


while(1):

    settings=json.dumps(getFromControl())
    handler=ControlHandler()
    handler.insertcontrolmessage(settings)
    time.sleep(5)
    processCleanUp("inputDeamon.py")
    processCleanUp("outputdeamon.py")
    procinput.kill()
    procoutput.kill()
    procinput = subprocess.Popen(['python', dir_path + '/inputdeamon/inputDeamon.py'])
    procoutput = subprocess.Popen(['python', dir_path + '/outputdeamon/outputdeamon.py'])







