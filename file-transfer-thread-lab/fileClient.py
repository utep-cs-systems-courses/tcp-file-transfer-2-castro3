#! /usr/bin/env python3

# Client program
import socket, sys, re

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


# loop through the server program
while True:
    try: # get a token to check if the connection worked
        token = framedSocket.receive(False).decode()
        print("Token: %s" %token)
    except ConnectionResetError:
        print("Lost connection to server...")
        break

    file = str(input('File: ')) # input from user
    fileTokens = re.split(' +', file)
    data = ''  # data that will be in the file provided

    #parse tokens
    if len(fileTokens) == 3:
        comm = fileTokens[0]
        localFile = fileTokens[1]
        remoteFile = fileTokens[2]
    elif len(fileTokens) == 2:
        comm = fileTokens[0]
        localFile = fileTokens[1]
        remoteFile = fileTokens[2]
    elif fileTokens[0] == 'exit': #end client if exit is inputted
        framedSocket.Send(clientSocket, fileTokens[0].encode(), False)
        break
    else:
        comm = None
        localFile = None
        remoteFile = None

    if comm == 'put':
        try: # make sure the file the user inputted exists and its valid
            path = './' + localFile
            fileInput = open(path, 'r')
        except FileNotFoundError:
            print("File %s does not exist" %localFile)
            fileInput = None
            data = None
        except PermissionError:
            print("Invalid Address")
            fileInput = None
            data = None

        if data is not None: # add data
            data = fileInput.readlines()
            if fileInput:
                for d in range(len(data)):
                    data[d] = token + "- " + localFile + ": " + data[d]

                for info in data:
                    print("Sending: %s" %info, end='')
                    framedSocket.Send(clientSocket, token.encode(), False)

                fileInput.close() # finish with file
                token = str(int(token) + 1)
                framedSocket.Send(clientSocket, token.encode(), False)
                
    else:
        print("File %s does not exist or has no data" %localFile)
        print("put <local-file> <remote-file>")
        framedSocket.Send(clientSocket, token.encode(), False)
            
clientSocket.close()
