#! /usr/bin/env python3

# Client program
import socket, sys, re, os

sys.path.append('./lib') # for params
import params

sys.path.append('./framed-echo')
from encapFramedSock import EncapFramedSock


switchesVarDefaults = (
    (('-s', '--server'),'server', "127.0.0.1:50001"),
    (('-p', '--proxy'), 'proxy', False), # boolean (set if present)
    (('-?', '--usage'), 'usage', False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)
server, proxy, usage = paramMap['server'], paramMap['proxy'],paramMap['usage']

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(':', server)
    serverPort = int(serverPort)

except:
    print("ERROR: Can't parse server:port from '%s'" %server)
    sys.exit(1)


addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

clientSocket = socket.socket(addrFamily, socktype)

if clientSocket is None:
    print('Could not open socket')
    sys.exit(1)

clientSocket.connect(addrPort)
framedSocket = EncapFramedSock((clientSocket, addrPort))

while True:
    filename = input("Enter file: ")
    filename.strip()

    # exit client
    if filename == "exit":
        sys.exit(0)
    else:
        if not filename:
            continue
        elif os.path.exists(filename):
            # open file and get data 
            file = open(filename, "rb")
            data = file.read()

            if len(data) < 1:
                print("File %s, is empty" % filename)
                continue

            framedSocket.send(filename, data)
            print("Sending file...")

        # file does not exists 
        else:
            print("ERROR: file %s not found. Try again" % filename)

    
            
clientSocket.close()
