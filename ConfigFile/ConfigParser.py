import os
import xml.etree.ElementTree as xparse

import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)
from Utils.NextNode import NextNode

class ConfigMonitor:

    def __init__(self,filepath='config.xml'):
        self.config = xparse.parse(filepath)
        self.ip=self.config.getiterator("ip")[0].text
        self.port = self.config.getiterator("port")[0].text
        self.name=self.config.getiterator("name")[0].text
        self.program = self.config.getiterator("program")[0].text


    def getPort(self):
        try:
            print self.port
            return int(self.port)

        except:
            print "Port must be integer"
            return None

    def getIp(self):
        return self.ip

    def getName(self):
        return self.name

    def getProgramName(self):
        return self.program

    def getNextNodeList(self):
        nodelist=[]
        nextlist=self.config.getiterator("nextnode")
        for node in nextlist:
            tempnode=NextNode(node.find("toip").text , node.find("toport").text)
            nodelist.append(tempnode)
        return nodelist

    def getInputDaemonPort(self):
        inpport = self.config.getiterator("inpport")[0].text
        return inpport

    def getOutputPort(self):
        outport = self.config.getiterator("outport")[0].text
        return outport

    def getOutputIP(self):
        outip = self.config.getiterator("outip")[0].text
        return outip





