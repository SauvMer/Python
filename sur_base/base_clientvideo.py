import socket
from time import sleep
import sys, os
from threading import Thread
import select

import numpy

if (sys.version_info > (3, 0)):
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty

class videoclient(Thread):

    HOST = ''
    PORT = 5001

    def __init__(self, host, port, video_queue):
        super(videoclient, self).__init__()
        self.running = True

        # Define server address
        self.HOST = host
        self.PORT = port

        # Connect with server
        self.wait_connect()

        self.video_queue = video_queue

    def wait_connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
        self.sock.connect((self.HOST, self.PORT))
        print("Socket connected")

    def run(self):
        n = 0
        while self.running:

            try:
                ready_r, ready_w, in_error = select.select([self.sock,],[self.sock,],[],5)
            except select.error:
                self.sock.shutdown(2)
                self.sock.close()
                print("Connection lost")
                self.wait_connect()

            # Receive
            if len(ready_r) > 0:
                length = recvall(self.sock,16)
                stringData = recvall(self.sock, int(length))
                #print("New frame received: %d"%(n))
                data = numpy.fromstring(stringData, dtype='uint8')
                self.video_queue.put(data)
                n += 1
            

        self.sock.close()

    def end(self):
        self.running = False

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf