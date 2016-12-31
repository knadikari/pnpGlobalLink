import json
import os
import socket

import time

import sys

from queuelib.queue import FifoSQLiteQueue

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

from termcolor import colored, cprint
from DB.DataBase import SQLDB

from ControlMessageHandler import MessageHandle
from Utils.NextNode import NextNode
from Utils.NodeDiscovery import NodeFinder

class ControlDeamon:
    def __init__(self):  #At initilasisation phase it will read the config and config itself
        self.db = SQLDB()
        self.ListenIP = ''
        self.ListenPORT = int(self.db.getControlDaemonPort())
        self.BufferSize = 1024





    def connect(self):
        try:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.bind((self.ListenIP, self.ListenPORT))
            self.serversocket.listen(1)  # Currenly listen to one
            return True
        except Exception as e:
            print e,"DemonListner @connect()"
            return False

    def handleClient(self):
        reply="********"
        gofornode=False
        while True:
            print "Control daemon standby"
            clientsock, clientaddr = self.serversocket.accept()

            print "Connection establish with client:- ", clientaddr
            totalclientdata=""

            while True:  # Will read the pipe untill no of { and no of } matches. [Parserble]
                jsonmsg=None
                ctime = time.time() #Get the current time for the check connection errors
                clientdata = clientsock.recv(self.BufferSize)#get the control message from previous node
                totalclientdata=totalclientdata+clientdata
                ctimenow = time.time()
                if(ctimenow==ctime):
                    break
                ctime=ctimenow
                try:
                    jsonmsg=json.loads(totalclientdata)  #Json is parsable means json is ccompletely receved
                    gofornode=True
                    break
                except Exception as e:
                    print e," while capturing the json commnd string ",

            prgid=jsonmsg["prgid"]
            curpid=self.db.getprgid()
            if(curpid=="01"):
                curpid=prgid  #Trick to find is this the first program Iot device will participate
            copyoriginaljson=json.loads(json.dumps(jsonmsg))
            #print "\n",totalclientdata
            isavilable=True
            reply = {}
            reply["msg"] = "Done"
            reply["iam"]=jsonmsg["you"]
            reply["myips"] = jsonmsg["you"]

            try:
                lengthofprg = len(jsonmsg["seq"])  #Sequence want send in the
            except:
                pass
            msgtype = jsonmsg["msgtype"]
            handle=MessageHandle()
            try:
                tempmyseqid=handle.getMySeqId(jsonmsg,jsonmsg["you"])
            except:
                pass
###################################
            cprint(self.db.getStatus()+"  "+prgid+"   "+curpid+"  ", 'red')

            if(msgtype=="link"):
                successip=None
                successPort=None
                if(gofornode):#ToDO check the status and return I cant message
                    if (self.db.getStatus() != "av" and prgid!=curpid):
                        cprint(' not av', 'green')
                        isavilable=False
                        reply["msg"] = "Fail"
                        reply["next"] = None
                    if(isavilable):  #this node is avilable
                        cprint('in av', 'green')
                        nodeFind=NodeFinder()
                        nextList, jsonmsg, handle, reply,successip,successPort =nodeFind.finder(jsonmsg,handle,reply,successip,successPort)
                        #handle=MessageHandle()
                        #nextList= handle.getNextNodes(jsonmsg)
                        # if(nextList!=None):  #This is not an end node
                        #     cprint('Not Last', 'green')
                        #     jsonmsg["you"] = handle.findNext(jsonmsg, jsonmsg["you"])["name"] #change the next node's you tag.
                        #     for node in nextList: #check all nodes sequentially for the availability
                        #         cprint('an node '+node.getip(), 'green')
                        #         if(not self.filetrOutSelfIps(node)):
                        #             #print "Done"
                        #             cprint('not loop', 'green')
                        #
                        #             msg=self.conectToNextNode(node,jsonmsg)#This means the node is available
                        #             if(msg):
                        #                 cprint('msg up', 'green')
                        #                 #print msg
                        #                 print "======================"
                        #                 if(not ("Fail" in json.loads(msg)["msg"])):
                        #                     cprint('Fail not in', 'green')
                        #                     tempjm=json.loads(msg)
                        #                     tempjm["ip"]=node.getip()
                        #                     reply["next"]=tempjm
                        #                     successip=node.getip()
                        #                     successPort=8200
                        #                     #print "------ ",msg
                        #                     break
                        #                 else:
                        #                     cprint('Fail in', 'green')
                        #             else:
                        #                 cprint('msg is False', 'green')
                        #                 pass
                        #         else:
                        #             cprint('loop broo', 'green')
                        #             print "Loop detected"
                        # else:#ToDo NEED TO GET THE PROGRAM NAME FROM THE MESSAGE
                        #     cprint('Last', 'green')
                        #     #print "HEY AM I THE LAST ONE?"
                        #     pass

                print nextList, jsonmsg, handle, reply,successip,successPort
                repmsg=json.dumps(reply)

                next_word_count=repmsg.count("next")
                cprint(""+str(lengthofprg)+" "+str(tempmyseqid)+" "+str(next_word_count), 'green')
                if((lengthofprg-tempmyseqid)==next_word_count):
                    cprint('LAMO My Parent:- '+clientaddr[0], 'green')
                    self.db.setParent(clientaddr[0])
                    try:
                        cprint(reply["next"],"yellow")
                    except:
                        print "error in printing reply json"
                    handle.WriteJsonFileOriginal(copyoriginaljson)
                    self.db.setControlJson(json.dumps(copyoriginaljson))
                    self.db.setSeqJson(json.dumps(repmsg))
                    handle.WriteJsonFile(repmsg)
                    self.db.setStatus(True)
                    self.db.setPrgID(prgid)
                    self.db.setMyName(copyoriginaljson["you"])
                    self.db.setOutputIp(successip)
                    self.db.setOutputPort(successPort)
                    controlq = FifoSQLiteQueue("/tmp/control.db")
                    controlq.push("doneeee Lamoo")

                    # path = "/tmp/control"
                    # try:
                    #     os.mkfifo(path)
                    # except Exception as e:
                    #     pass
                    # fifo = open(path, "w")
                    # fifo.write("doneeee Lamoo")
                    # fifo.close()

                clientsock.send(repmsg)
                #print len(reply)
                clientsock.close()
            elif(msgtype=="update"):
                handle=MessageHandle()
                #obj=handle.getSeqJonObj()
                #print "--**--",obj["next"]
                #obj["next"] =jsonmsg
                #print "'---",obj["next"]
                #clientsock.sendall("-----")
                #self.sendToParent(json.dumps(obj))
                #clientsock.close()

                print "----"
            #if(msgtype=="update"):

    def sendToParent(self,msg):
        parent=NextNode(self.db.getParent(), 8100,0)
        parent.sendMessageToParent(msg)

cprint("DaemonListner start","yellow")
cont = ControlDeamon()
if (cont.connect()):
    cont.handleClient()
