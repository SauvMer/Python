import socket
from time import sleep
import sys, os
from threading import Thread
import select

if (sys.version_info > (3, 0)):
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty

class client(Thread):

    HOST = ''
    PORT = 5000

    def __init__(self, host, port, rece_queue, send_queue):
        super(client, self).__init__()
        
        # Define server address
        self.HOST = host
        self.PORT = port

        # Connect with server
        self.wait_connect()

        self.rece_queue = rece_queue
        self.send_queue = send_queue

    def wait_connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
        self.sock.connect((self.HOST, self.PORT))
        print("Socket connected")


    def run(self):
        while 1:

            try:
                ready_r, ready_w, in_error = select.select([self.sock,],[self.sock,],[],5)
            except select.error:
                self.sock.shutdown(2)
                self.sock.close()
                print("Connection lost")
                self.wait_connect()

            # Receive
            if len(ready_r) > 0:
                data = self.sock.recv(256).decode()
                data = data.split("$")
                for k in range(0, len(data)-1):
                    print(data[k])
                    self.rece_queue.put(data[k])
            # Send
            if len(ready_w) > 0:
                try:
                    msg = self.send_queue.get_nowait() + "$"
                    self.sock.sendall(msg.encode())
                    if(msg.startswith("END")):
                        break
                except Empty:
                    pass

        self.sock.close()

    def end(self):
        self.running = False