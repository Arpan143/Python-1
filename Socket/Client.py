#!/user/bin/env python
# -*- coding: utf-8 -*-

import socket
from time import ctime

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpCliSock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpCliSock.connect(ADDR)

def Client():
    while True:
        data = raw_input('> ')
        if not data:
            break
        tcpCliSock.send(data)
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        print 'Service say:',data
    tcpCliSock.close()

Client()
