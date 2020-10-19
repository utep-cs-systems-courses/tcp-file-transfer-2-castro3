#!/usr/bin/env python3

import socket, re, sys, os

sys.path.append('./lib')

import params

sys.path.append('./framed-echo')

from encapFramedSock import EncapFramedSock

from threading import Thread

switchesVarDefaults = (
    (('-l', '--listentPort'), 'listenPort', 50001),
    (('-p', '--proxy'), 'proxy', False),
    (('-?', '--usage'), 'usage', False)
    )


paramMap = params.parseParams(switchesVarDefaults)
listenPort, proxy, usage = paramMap['listenPort'], paramMap['proxy'], paramMap['usage']


if usage:
    params.usage()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
serverSocket.bind(bindAddr)
serverSocket.listen(5)
print("listening to client...")


class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)

    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            payload = self.fsock.receive(False)
            if not payload:
                self.fsock.close()
                return
            payload += b"!"
            self.fsock.send(payload, False)


while True:
    sockAddr = serverSocket.accept()
    server = Server(sockAddr)
    server.start()
