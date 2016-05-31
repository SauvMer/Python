import socket
from threading import Thread
import select

import sys
if (sys.version_info > (3, 0)):
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty

class server(Thread):

    HOST = ''
    PORT = 5000

    def __init__(self, port, rece_queue, send_queue):
        super(server, self).__init__()
        self.running = True

        # Define server address
        self.PORT = port

        # Connect with client
        self.wait_connect()

        # Define receiving queue
        self.rece_queue = rece_queue
        self.send_queue = send_queue


    def wait_connect(self):
        # Creation du socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
        self.sock.bind((self.HOST, self.PORT))
        print("Socket bind completed")
        self.sock.listen(1)
        self.connection, self.client_address = self.sock.accept()

    def run(self):
        while self.running:
            #print("Drone server running")
            # Check connection state
            try:
                ready_r, ready_w, in_error = select.select([self.connection,],[self.connection,],[],5)
            except select.error:
                self.connection.shutdown(2)
                self.connection.close()
                print("Connection lost")
                self.wait_connect()
            
            # Receive
            if len(ready_r) > 0:
                data = self.connection.recv(256).decode()
                data = data.split("$")
                for k in range(0, len(data)-1):
                    self.rece_queue.put(data[k])
                    if(data[k].startswith("END")):
                        break
            # Send
            if len(ready_w) > 0:
                try:
                    msg = self.send_queue.get_nowait() + "$"
                    #print(msg)
                    self.connection.sendall(msg.encode())
                except Empty:
                    pass


if __name__ == "__main__":

    # IMPORT
    import sys, os
    if (sys.version_info > (3, 0)):
        from queue import Queue, Empty
    else:
        from Queue import Queue, Empty

    rece_queue = Queue()
    send_queue = Queue()
    ser = server(int(sys.argv[1]), rece_queue, send_queue)
    ser.start()
    while 1:
        pass