import json
import socket

clientsocket=socket.socket()

#138.197.26.183   0001
#138.197.30.34     0002
#138.197.8.95      0003
#192.34.63.88      0004

#ConnetTo="138.197.26.183"
ConnetTo="138.197.26.183"
Port=8100;
BufferSize=1024
data={}
data["seq"]=[{"seqno":1,"name":"a"},{"seqno":2,"name":"b"},{"seqno":3,"name":"c"}]#,{"seqno":4,"name":"d"}]
data["you"]="a" #you means the node name
data["a"]=[{"ip":"192.168.1.70","conport":8100,"avialable":0,"inport":8090},{"ip":"138.197.26.183","conport":8080,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090}]
data["b"]=[{"ip":"192.168.1.20","conport":8100,"avialable":0,"inport":8090},{"ip":"138.197.30.34","conport":8100,"avialable":0,"inport":8090},{"ip":"138.197.8.95","conport":8080,"avialable":0,"inport":8090}]
#data["c"]=[{"ip":"127.0.0.1","conport":8100,"avialable":0,"inport":8090},{"ip":"138.197.30.34","conport":8100,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090}]
data["c"]=[{"ip":"127.0.0.1","conport":8100,"avialable":0,"inport":8090},{"ip":"192.34.63.88","conport":8100,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090}]
data["prgid"]="125899"
data["msgtype"]="link"


#data["tee"]=[{"node":"a","ip":"127.0.0.1","port":100},{"node":"b","ip":"127.0.0.1","port":100},{"node":"c","ip":"127.0.0.1","port":100},{"node":"d","ip":"127.0.0.1","port":100}]



datatee={}
datatee["seq"]=[{"seqno":1,"name":"d"}]
datatee["you"]="d"
datatee["d"]=[{"ip":"127.0.0.1","conport":8100,"avialable":0,"inport":8090},{"ip":"192.34.63.88","conport":8100,"avialable":0,"inport":8090},{"ip":"127.0.0.1","conport":8080,"avialable":0,"inport":8090}]
datatee["prgid"]="125899"
datatee["msgtype"]="link"
datatee["tee"]=[{"node":"a","data":None},{"node":"b","data":None},{"node":"c","data":None},{"node":"d","data":None}]


data["tee"]=[{"node":"a","data":None},{"node":"b","data":datatee},{"node":"c","data":None},{"node":"d","data":None}]



recoverygen={"msg": "Done", "iam": "b", "myips": "b", "next": {"next": {"msg": "Done", "iam": "c", "ip": "138.197.8.95", "myips": "c", "next": {"msg": "Done", "iam": "d", "myips": "d", "ip": "192.34.63.88"}}}}
recoverygen["msgtype"]="update"
recoverygen["prgid"]="125899"
recoverygen["you"]="a"
msg=json.dumps(data)
{"ip":"192.168.1.2","conport":8100,"avialable":0,"inport":8090}

#print msg



clientsocket.connect((ConnetTo,Port))

fullmsg=""
#while True:
clientsocket.sendall(msg)
print clientsocket.recv(2048)

#print len(fullmsg)
clientsocket.close()