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
serverSocket.listen(2)
print("listening to client...")


# loop through server receiving files
while True:
    sock, addr = serverSocket.accept()
    framedSend(sock, token.encode(), False)

    if not os.fork():
        while True:
            data = framedReceive(sock, False).decode()
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
                framedSend(sock, token.encode(), False)
                print("Sending... Token: " + token)

            else:
                token = infoData[0]
                file = infoData[1]
                fileData = infoData[2]

                if file is not None:
                    path = './' + file
                    file = open(path, 'a')
                    file.write(fileData)
                    print("Writing to " + file)
                    file.close()
                else:
                    print(file + " is on server")


        sock.close()
