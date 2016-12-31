import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.sendto('Hello!', 'pipe_test.fifo1')
