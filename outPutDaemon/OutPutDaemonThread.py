import os
import socket

import sys

import time

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)


from ConfigFile.ConfigParser import ConfigMonitor
from OutputHandler import outputHandler
from DB.DataBase import SQLDB
from termcolor import colored, cprint

class OutputDaemon:
    def __init__(self):
        self.db = SQLDB()
        self.ip=self.db.getOutputDaemonIP()
        self.port=self.db.getOutputDaemonPort()

    def connect(self):
        if(self.ip is None):
            while(True):
                demonvar=1

        try: ##when done in here all thread must be activated
            #for i in self.ip:
            self.clientsocket=socket.socket()
            self.clientsocket.settimeout(2)
            self.clientsocket.connect((self.ip,int(self.port)))
            self.handle=outputHandler()
            return True
        except Exception as e:
            #print "Error at output:- ",e
            return False

    def sendmsg(self):
        while True:
            try:
                msg=self.handle.getmsg()
                self.clientsocket.send(msg)
            except Exception as e:
                print "Outputdaemn ",e
                break
        self.clientsocket.close()


cprint("OutputDaemon start","yellow")
outp = OutputDaemon()
failcount = 0;
while (True):
    if (outp.connect()):
        print "Connected"
        outp.sendmsg()
    # break
    print "Error @ Output"
    failcount = failcount + 1
    if (failcount > 5):
        print "Next Down"
        # recoverNext()
        break
    time.sleep(2)

