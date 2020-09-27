#Oscar Castro
#!/usr/bin/env python3

# Client program
import socket, sys, re

sys.path.append("../lib") # for params
import params

from framedSock import frameSend, framedReceive


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
