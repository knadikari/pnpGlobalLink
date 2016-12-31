import json
import os
import socket
import netifaces
import time
from termcolor import colored, cprint
import sys



path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)


class NodeFinder:
    def __init__(self):
        self.myips = self.getAllInterfaceAddresses()  # This will be keep all his ips.

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

        #if (node.getip() in self.myips):
        #    return True
        if ("127.0." in node.getip()):
            return True
        return False

    def conectToNextNode(self, NextNode, msg):
        try:
            return NextNode.checkStatus(msg)
        except:
            return False


    def finder(self,jsonmsg,handle,reply,successip,successPort):
        nextList = handle.getNextNodes(jsonmsg)
        if (nextList != None):  # This is not an end node
            cprint('Not Last', 'green')
            jsonmsg["you"] = handle.findNext(jsonmsg, jsonmsg["you"])["name"]  # change the next node's you tag.
            for node in nextList:  # check all nodes sequentially for the availability
                cprint('an node ' + node.getip()+" - "+str(node.getport()), 'green')
                if (not self.filetrOutSelfIps(node)):
                    # print "Done"
                    cprint('not loop', 'green')

                    msg = self.conectToNextNode(node, jsonmsg)  # This means the node is available
                    if (msg):
                        cprint('msg up', 'green')
                        # print msg
                        print "======================"
                        if (not ("Fail" in json.loads(msg)["msg"])):
                            cprint('Fail not in', 'green')
                            tempjm = json.loads(msg)
                            tempjm["ip"] = node.getip()
                            reply["next"] = tempjm
                            successip = node.getip()
                            successPort = 8200
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
        return nextList, jsonmsg, handle, reply,successip,successPort