import socket


s = socket.socket()  # Create a socket object
host = ''  # Get local machine name
port = 8090  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(5)  # Now wait for client connection.
while True:
    c, addr = s.accept()  # Establish connection with client.
    print 'Got connection from', addr
    #c.send('Thank you for connecting')
    while 1:
        m=c.recv(1024)
        print m
        if(not m):
            break
    c.close()  # Close the connection

exit()



ListenIP='';
ListenPORT=8150;
BufferSize=1024

serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serversocket.bind((ListenIP,ListenPORT))

serversocket.listen(1)  #Currenly listen to one

bigreply=""
for i in range(0,1000):
    bigreply=bigreply+str(i)+" "

while True:
    clientsock,clientaddr=serversocket.accept()
    print "Connection establish with client:- ", clientaddr

    while True:
        print "wait fro recv"
        clientdata=str(clientsock.recv(BufferSize))
        if(not clientdata):
            break
        #clientsock.send(bigreply);
        print clientdata
    clientsock.close()
print "Socket is created"