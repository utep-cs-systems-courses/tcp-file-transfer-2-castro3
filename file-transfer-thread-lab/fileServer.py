#!/usr/bin/env python3

import socket, re, sys, os, time, threading

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

lock = threading.Lock()


class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.threadSock = EncapFramedSock(sockAddr)

    def write_file(self, filename, data):
        try:
            # check if the dir exists else create it
            if not os.path.exists("./serverFiles/"):
                os.makedirs("./serverFiles/")

            # create the file and write to it.
            file_writer = open("./serverFiles/" + filename, 'w+b')
            file_writer.write(data)
            print("Writing to file...")

            # close file
            file_writer.close()
            print("file %s was recieved from address %s" %(filename, self.addr))
        except FileNotFoundError:
            print("ERROR: file %s not found " % filename)
            sys.exit(1)

    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            filename, data = self.threadSock.receive()
            
            # if data was not received close client
            if filename is None or data is None:
                print("client ", self.addr, " disconnected")
                sys.exit(0)

            lock.acquire()

            # write to file and save it
            filename = filename.decode()
            print(self.addr, " will attempt to save file %s" % filename)
            self.write_file(filename, data)

            lock.release()


while True:
    sockAddr = serverSocket.accept()
    server = Server(sockAddr)
    server.start()
