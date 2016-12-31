import json
import os

import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

from Utils.NextNode import NextNode

class MessageHandle:

    def WriteJsonFileOriginal(self,jsonobj):  #write the requested json file into file
        path=os.getenv("HOME")+"/MetaPnpGlobal"
        if not os.path.exists(path):
            os.makedirs(path)
        filepath=path+"/config.json"
        jsfile=open(filepath,"w")
        json.dump(jsonobj, jsfile)

    def WriteJsonFile(self,jsonobj): #write success file into json file
        path=os.getenv("HOME")+"/MetaPnpGlobal"
        if not os.path.exists(path):
            os.makedirs(path)
        filepath=path+"/configseq.json"
        jsfile=open(filepath,"w")
        #json.dump(jsonobj, jsfile)
        jsfile.write(json.dumps(jsonobj))


    def getMySeqId(self,fulljson,myprogram):
        sequence = fulljson["seq"]
        myseqno = -1
        for i in sequence:
            if (i["name"] == myprogram):
                myseqno = i["seqno"]
                break
        return myseqno

    def getSeqJonObj(self):
        path = os.getenv("HOME") + "/MetaPnpGlobal"
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = path + "/configseq.json"
        jsfile = open(filepath, "r")
        strjs=jsfile.read()
        jobj=json.loads(strjs)
        jobj = json.loads(jobj)
        return jobj




    def findNext(self,fulljson, myprogram):
        sequence = fulljson["seq"]
        myseqno = -1
        for i in sequence:
            if (i["name"] == myprogram):
                myseqno = i["seqno"]
                break
        if (myseqno == len(sequence)):
            return None
        if (myseqno == -1):
            return False
        if (myseqno != -1):
            for i in sequence:
                if (i["seqno"] == myseqno + 1):
                    return i

    def getNextNodes(self,fulljson):
        myprg=fulljson["you"]
        nextmeta=self.findNext(fulljson,myprg)
        if(nextmeta!=None):
            nextList=fulljson[nextmeta["name"]]
            nextReturnList=[]
            for i in nextList:
                if(i["avialable"]!=-1):
                    nextReturnList.append(NextNode(i["ip"], i["conport"],i["inport"]))
            return nextReturnList
        else:
            return None

    def getNextTeeNodes(self, fullteejson):
        nextReturnList=[]
        #fullteejson=json.loads(fullteejson)
        for i in fullteejson:
            print i
            nextReturnList.append(NextNode(i["ip"], i["conport"], i["inport"]))
        return nextReturnList


# data={}
# data["seq"]=[{"seqno":1,"name":"a"},{"seqno":2,"name":"b"},{"seqno":3,"name":"c"},{"seqno":4,"name":"d"}]
# data["you"]="a"
# data["a"]=[{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090}]
# data["b"]=[{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090}]
# data["c"]=[{"ip":"127.0.100.1","conport":8080,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090}]
# data["d"]=[{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090}]
#
# print json.dumps(data)
#
# msg=json.dumps(data)
#
#
# recveddemo=json.loads(msg)
#
# a=MessageHandle()
# print a.getNextNodes(recveddemo)



