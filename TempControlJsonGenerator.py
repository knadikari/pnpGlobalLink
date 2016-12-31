"a|b|c"
import json

#name will be program name

import socket               # Import socket module

import time



s = socket.socket()
import socket  # Import socket module

    # Create a socket object
host = '192.168.1.3' # Get local machine name
port = 8080                # Reserve a port for your service.

s.connect((host, port))
while(True):
    for i in range(0,10000):
        s.sendall(str(i)+"---\n")
        print i
        time.sleep(1)
#print s.recv(1024)
s.close()

exit(0)


data={}
data["seq"]=[{"seqno":1,"name":"a"},{"seqno":2,"name":"b"},{"seqno":3,"name":"c"},{"seqno":4,"name":"d"}]
data["you"]="b"
data["a"]=[{"ip":"127.0.0.1","port":8080,"avialable":0},{"ip":"127.0.0.1","port":8080,"avialable":0},{"ip":"127.0.0.1","port":8080,"avialable":0}]
data["b"]=[{"ip":"127.0.0.1","port":8080,"avialable":0},{"ip":"127.0.0.1","port":8080,"avialable":0},{"ip":"127.0.0.1","port":8080,"avialable":0}]
data["c"]=[{"ip":"127.0.0.1","port":8080,"avialable":0},{"ip":"127.0.0.1","port":8080,"avialable":0},{"ip":"127.0.0.1","port":8080,"avialable":0}]
data["d"]=[{"ip":"127.0.0.1","port":8080,"avialable":0},{"ip":"127.0.0.1","port":8080,"avialable":0},{"ip":"127.0.0.1","port":8080,"avialable":0}]

print json.dumps(data)

msg=json.dumps(data)


recveddemo=json.loads(msg)

myprogram=recveddemo["you"]

def findNext(fulljson,myprogram):
    sequence=fulljson["seq"]
    myseqno=-1
    for i in sequence:
        if(i["name"]==myprogram):
            myseqno=i["seqno"]
            break
    if(myseqno==len(sequence)):
        return None
    if(myseqno==-1):
        return False
    if(myseqno!=-1):
        for i in sequence:
            if (i["seqno"] == myseqno+1):
                return i


print findNext(recveddemo,myprogram)
