# bind socket
import os
import socket

import fcntl

import errno



sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.bind('/tmp/100p3')
# set socket non-blocking
fcntl.fcntl(sock.fileno(), fcntl.F_SETFL)

# get a datagram
try:
    datagram = sock.recv(1024)
except (OSError, socket.error) as ex:
    if ex.errno not in (errno.EINTR, errno.EAGAIN):
        raise
else:
    print('Datagram: %r' % datagram)

