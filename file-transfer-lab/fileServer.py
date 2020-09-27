#Oscar Castro
#!/usr/bin/env python3

import socket, re, sys, os

sys.path.append('../lib')

import params

sys.path.append('../framed-echo')

from framedSock import framedReceive, framedSend





switchesVarDefaults = (
    (('-l', '--listentPort'), 'listenPort', 50001),
    (('-p', '--proxy'), 'proxy', False),
    (('-?', '--usage'), 'usage', False)
    )


paramMap = params.parseParams(switchesVarDefaults)
listenPort, proxy, usage = paramMap['listenPort'], paramMap['proxy'], paramMap['usage']


if usage:
    params.usage()


file = {}
token = '0'
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
serverSocket.bind(bindAddr)
serverSocket.listen(1)
print("listening on:", bindAddr)

sock, addr = serverSocket.accept()


