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


files = {}
file = ''
token = '0'
fileData = ''

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("", listenPort)
serverSocket.bind(bindAddr)
serverSocket.listen(1)
print("listening to client...")

sock, addr = serverSocket.accept()
sock.send(token.encode()) if not proxy else framedSend(sock, token.encode(), False)

# loop through server receiving files
while True:
    data = sock.recv(1024).decode() if not proxy else framedSend(sock, False)
    if not data:
        if file not in files:
            print("File not found")
        break

    if proxy:
        data = data.decode()

    if data == "exit":
        break

    infoData = re.split(":", data)
    if len(infoData) == 1:
        token = infoData[0]
        files[file] = -1
        file = None
        fileData = None
        sock.send(token.encode()) if not proxy else framedSend(sock, token.encode(), False)
        print("Sending... Token: " + token)

    else:
        print(infoData)
        token = infoData[0]
        file = infoData[1]
        fileData = infoData[2]

    if file is None:
        path = './' + file
        file = open(path, 'a')

        file.write(fileData)
        file.close()


sock.close()
