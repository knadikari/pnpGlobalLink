

import os

import time

import sys



path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

from ControlDeamonListen.DeamonListner import ControlDeamon
from inputDaemonListen.inpuDeamon import inputDaemon
from outPutDaemon.OutPutDaemon import OutputDaemon

def controlDaemonFunct():
    cont=ControlDeamon()
    if(cont.connect()):
        cont.handleClient()

def inputDaemonFunc():
    inpt=inputDaemon()
    if(inpt.connect()):
        inpt.handleClient()

def ouputFunc():
    outp=OutputDaemon()
    failcount=0;
    while(True):
        if(outp.connect()):
            print "Connected"
            outp.sendmsg()
        #break
        print "Error @ Output"
        failcount=failcount+1
        if(failcount>5):
            print "Next Down"
            #recoverNext()
            break
        time.sleep(2)

ouputFunc()

exit(0)

try:
    path = os.getenv("HOME") + "/MetaPnpGlobal"
    if not os.path.exists(path):
        print "---"
        os.makedirs(path)
except Exception as e:
    print e
filepath = path + "/config.json"
print filepath
try:
    confile=open(filepath,'r')
except Exception as e:
    print"at MainHandler"
    confile = open(filepath, 'w+')
    confile.close()
    confile = open(filepath, 'r')
msg=confile.read()
if(msg!=None):
    curmdh=md5(msg)
else:
    curmdh=None
confile.close()



#controlDaemonFunct()

#inputDaemonFunc()

#ouputFunc()

controid=os.fork()
if(controid==0):
    print "Control"
    controlDaemonFunct()
else:

    inpid=os.fork()
    if(inpid==0):
        print "Inp"
        inputDaemonFunc()
    else:

        outid=os.fork()
        if(outid==0):
            print "Out"
            ouputFunc()

        else:
            while True:
                confile = open(filepath)
                msg = confile.read()
                if (msg != None):
                    newmdh = md5(msg)
                else:
                    newmdh = None
                confile.close()
                if (curmdh != newmdh):
                    print "Got File Change"
                time.sleep(5)
