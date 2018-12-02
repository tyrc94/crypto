#!/usr/bin/python3

''' 
Very simple implementation of an encrypted chat (using RSA) 
This is very insecure: keys can easily be retrieved if an adversary was
monitoring the connection
'''


import socket
import threading
import sys
import json

from rsa import RSA

priv = RSA(128)
priv.generate_keypair(*(priv.generate_primes()))

class Server:
    sock = socket.socket()
    connections = []
    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen()

    def handler(self, c, a):
        while True:
            data = c.recv(8192)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0]) + ":" + str(a[1]), "disconnected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ":" + str(a[1]), "connected")


class Client:
    sock = socket.socket()

    def send_message(self):
        while True:
            message = input("")
            payload = dict(sender=self.sock.getsockname(),
                            bitsize = priv.bits,
                            pk = priv.pk,
                            sk = priv.sk,
                            message=priv.encrypt(message))

            msg_dump = json.dumps(payload)

            self.sock.send(bytes(msg_dump, "utf-8"))

    def __init__(self, address):
        self.sock.connect((address, 10000))

        iThread = threading.Thread(target=self.send_message)
        iThread.daemon = True
        iThread.start()
        while True:
            data = self.sock.recv(8192)
            if not data:
                break
            data = json.loads(data)
            if data['sender'] == list(self.sock.getsockname()):
                print("<You> " + RSA(data['bitsize'], data['pk'], data['sk']).decrypt(data['message']))
            else:
                print("<" + data['sender'][0] + ":" + str(data['sender'][1]) + "> " + RSA(data['bitsize'], data['pk'], data['sk']).decrypt(data['message']))


if len(sys.argv) > 1:
    

    client = Client(sys.argv[1])

else:
    server = Server()
    server.run()

