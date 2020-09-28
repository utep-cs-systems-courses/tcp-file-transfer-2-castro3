#Oscar Castro
#!/usr/bin/env python3

# Client program
import socket, sys, re

sys.path.append('../lib') # for params
import params

sys.path.append('../framed-echo')
from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-p', '--proxy'), "proxy", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)
server, proxy, usage = paramMap['server'], paramMap['proxy'],paramMap['usage']

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(':', server)
    serverPort = int(serverPort)

except:
    print('ERROR: Can\'t parse server:port from %s' %server)
    sys.exit(1)


addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

clientSocket = socket.socket(addrFamily, socktype)

if clientSocket is None:
    print('Could not open socket')
    sys.exit(1)

clientSocket.connect(addrPort)


# loop through the server program
while True:
    try: # get a token to check if the connection worked
        token = clientSocket.recv(1024).decode() if not proxy else framedSend(clientSocket, False)
        print("Token: %s" %token)
    except ConnectionResetError:
        print("Lost connection to server...")
        break

    file = input('Enter name of file: ') # input from user
    data = ''  # data that will be in the file provided
    if file == 'exit':
        clientSocket.send(file.encode()) if not proxy else frameSend(clientSocket,
                                                                     file.encode(), False)
        break

    try: # make sure the file the user inputted exists
        path = './' + file
        fileInput = open(path, 'r')
    except FileNotFoundError:
        print("File %s does not exist" %file)
        file = None
        data = None

    if data is not None: # add data
        data = fileInput.readlines()
        if fileInput:
            for d in range(len(data)):
                data[d] = token + ", " + file + ": " + data[d]

            for info in data:
                print("Sending: %s" %info, end='')
                clientSocket.send(info.encode()) if not proxy else frameSend(clientSocket,
                                                                             info.encode(), False)
            fileInput.close() # finish with file
            token = str(int(token) + 1)
            clientSocket.send(token.encode()) if not proxy else framedSend(clientSocket,
                                                                           token.encode(), False)

    else:
        print("File %s does not exist or has no data" %file)
        clientSocket.send(token.encode()) if not proxy else framedSend(clientSocket,
                                                                       token.encode(), False)
            
clientSocket.close()
