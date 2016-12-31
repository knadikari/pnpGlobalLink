import json
import os
import subprocess

import time

import sys

from termcolor import cprint

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)


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



path = "/tmp/control"
try:
    os.mkfifo(path)
except Exception as e:
    pass


processCleanUp("inputDeamon.py")
processCleanUp("OutPutDaemon.py")

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

proccontrol = subprocess.Popen(['python', dir_path+'/ControlDeamonListen/DeamonListner.py'])
procinput = subprocess.Popen(['python', dir_path+'/inputDaemonListen/inpuDeamon.py'])
procoutput = subprocess.Popen(['python', dir_path+'/outPutDaemon/OutPutDaemon.py'])
process = subprocess.Popen(['python', dir_path+"/Program/programhandle.py"])

def getFromControl():
    fifo = open(path, "r")
    msg=fifo.read()
    print msg
    fifo.close()


while(1):
    cprint("Wait for control", "red")
    settings=json.dumps(getFromControl())
    time.sleep(5)
    cprint("got  control message and restarting", "red")
    #processCleanUp("inputDeamon.py")
    #processCleanUp("outputdeamon.py")

    #procinput.kill()
    procoutput.kill()
    #procinput = subprocess.Popen(['python', dir_path + '/inputDaemonListen/inpuDeamon.py'])
    procoutput = subprocess.Popen(['python', dir_path + '/outPutDaemon/OutPutDaemon.py'])

