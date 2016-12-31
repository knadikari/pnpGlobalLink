import json
import os

import sys
from termcolor import colored, cprint



path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

import netifaces

from DB.DataBase import SQLDB
from ControlDeamonListen.ControlMessageHandler import MessageHandle
from Utils.NextNode import NextNode

class RecoverDaemon:
    def __init__(self):
        try:
            self.myips = self.getAllInterfaceAddresses()  # This will be keep all his ips.
            self.db=SQLDB()
            path = os.getenv("HOME") + "/MetaPnpGlobal"
            if not os.path.exists(path):
                os.makedirs(path)
            filepath = path + "/config.json"
            jsfile = open(filepath, "r")
            cont=jsfile.read().strip()
            cprint(cont,'red')
            self.myreqjson =json.loads(cont)
            self.myreqjson = json.loads(self.db.getControlJson())
            path = os.getenv("HOME") + "/MetaPnpGlobal"
            if not os.path.exists(path):
                os.makedirs(path)
            filepathseq = path + "/configseq.json"
            jsfileseq = open(filepathseq, "r")
            cont = jsfileseq.read().strip()
            cprint(cont, 'red')
            self.myseqjson = json.loads(cont)
            self.myreqjson = json.loads(self.db.getControlJson())
            self.myseqjson = json.loads(self.db.getSeqJson())


            self.myseqjson=self.myseqjson.encode('ascii', 'ignore')
            self.myseqjson = json.loads(self.myseqjson)
            #self.myreqjson = self.myreqjson.encode('ascii', 'ignore')
            self.myid = self.myreqjson["you"]
            cprint(self.myseqjson, 'yellow')
            cprint(self.myreqjson, 'blue')
            #return  True
        except Exception as e:
            print e
            self.myreqjson=None
            self.myseqjson=None

    def getNextScans(self):
        if(self.myreqjson is None or self.myseqjson is None):
            return False
        else:
            reply = {}

            name=self.db.getMyName()
            ###REPLICATE FROM DEAMONLISTENR
            handle=MessageHandle()
            nextList = handle.getNextNodes(self.myreqjson)
            if (nextList != None):  # This is not an end node
                cprint('Not Last', 'green')
                self.myreqjson["you"] = handle.findNext(self.myreqjson, self.myreqjson["you"])["name"]  # change the next node's you tag.
                cprint(self.myreqjson["you"],'blue')
                for node in nextList:  # check all nodes sequentially for the availability
                    cprint('an node ' + node.getip(), 'green')
                    if (not self.filetrOutSelfIps(node)):
                        # print "Done"
                        cprint('not loop', 'green')
                        msg = self.conectToNextNode(node, self.myreqjson)  # This means the node is available
                        if (msg):
                            cprint('msg up', 'green')
                            # print msg
                            print "======================"
                            if (not ("Fail" in json.loads(msg)["msg"])):
                                cprint('Fail not in', 'green')
                                tempjm = json.loads(msg)
                                tempjm["ip"] = node.getip()
                                reply["next"] = tempjm
                                # print "------ ",msg
                                break
                            else:
                                cprint('Fail in', 'green')
                        else:
                            cprint('msg is False', 'green')
                            pass
                    else:
                        cprint('loop broo', 'green')
                        print "Loop detected"
            else:  # ToDo NEED TO GET THE PROGRAM NAME FROM THE MESSAGE
                cprint('Last', 'green')
                # print "HEY AM I THE LAST ONE?"
                pass
            #cprint(self.myseqjson["next"], 'red')
            #self.myseqjson["next"]=reply
            #print type(self.myseqjson)
            #print type(self.myseqjson.encode('ascii', 'ignore'))
            #repmsg = json.dumps(reply)

            #print len(repmsg.split("next"))," Len Rep Message"
            #print len(self.myreqjson.split("next")), " Len Rep Message"



            finalReply=json.loads(json.dumps(self.myseqjson))
            try:
                finalReply["next"]=reply["next"]
            except:
                finalReply["next"] = None




            if(self.getNoOfnodes(self.myseqjson)==self.getNoOfnodes(finalReply)):
                cprint('LAMO', 'green')


            #parent = NextNode(self.db.getParent(), 8100, 0)
            #parent.sendMessageToParent(repmsg)

            ##########END REPLICATE DEAMON LISTNER

    def getAllInterfaceAddresses(self):  # get the idea of the network address of the node has.
        iplist = []
        interface_list = netifaces.interfaces()
        for iname in interface_list:
            if (("eth" in iname) or ("wlan" in iname)):  # get only eth and wlan (ethernet and wifi addresses)
                try:
                    internetIps = netifaces.ifaddresses(iname)[netifaces.AF_INET]  # fetch only IPv4 address only
                    iplist.append(internetIps[0]["addr"])
                except:
                    pass
        return iplist

    def filetrOutSelfIps(self, node):

        if (node.getip() in self.myips):
            return True
        if ("127.0." in node.getip()):
            return True
        return False

    def conectToNextNode(self, NextNode, msg):
        try:
            return NextNode.checkStatus(msg)

        except:
            return False

    def getNoOfnodes(self,jsonobj):
        jsfile = jsonobj
        count = 0;
        while ("next" in jsfile):
            count = count + 1
            jsfile = jsfile["next"]
            if(jsfile is None):
                return count
            #cprint(jsfile,'grey')
        #cprint('------------','green')
        return count

p=RecoverDaemon()
p.getNextScans()



