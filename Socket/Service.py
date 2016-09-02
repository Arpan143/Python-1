#!/user/bin/env python
# -*- coding: utf-8 -*-

import socket
from time import ctime

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpSerSock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.bind(ADDR)  ##将主机、端口绑定
tcpSerSock.listen(5)  ##开启监听

def Service():
    while True:
        print 'waiting for connection....'
        tcpCliSock, address = tcpSerSock.accept()
        print '....connected from :' ,address

        while True:
            data = tcpCliSock.recv(BUFSIZ)
            if not data:
                break
            print address,' say ',data
            tcpCliSock.send(raw_input('> '))

    tcpCliSock.close()
    tcpSerSock.close()

Service()