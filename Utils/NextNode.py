import json
import os
import socket

import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

from socket import error as socket_error

class NextNode:
    def __init__(self,ipinp,ipport,inpInpPort=None):
        self.ip=ipinp
        self.port=ipport #control
        self.inputPort=inpInpPort


    def getport(self): #Retun the port of the current object
        try:
            return int(self.port)
        except:
            return None

    def getip(self):
        return self.ip

    def getConnectableObject(self):
        conlink=(self.getip(),self.getport())
        return conlink

    def checkStatus(self,msg):
        clientsocket = socket.socket()
        clientsocket.settimeout(2)
        clientsocket.connect(self.getConnectableObject())
        try:
            req_msg_json={}
            req_msg_json["type"]="checkstatus"
            #print "NextNode",msg
            clientsocket.sendall(json.dumps(msg))
            rep = clientsocket.recv(1024)
            print rep,"------"
            return rep
        except socket_error as s_err:
            print s_err," ppppp"
            if(s_err.errno==111):
                return False   #ToDo add return message type


    def sendMessageToParent(self,msg):
        clientsocket = socket.socket()
        clientsocket.settimeout(2)
        clientsocket.connect(self.getConnectableObject())
        try:
            req_msg_json = {}
            req_msg_json["type"] = "checkstatus"
            # print "NextNode",msg
            clientsocket.sendall(json.dumps(msg))
            #rep = clientsocket.recv(1024)
            #return rep
            return True
        except socket_error as s_err:
            print s_err, " ppppp"
            if (s_err.errno == 111):
                return False  # ToDo add return message type


