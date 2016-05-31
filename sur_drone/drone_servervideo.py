import socket
from threading import Thread
import select

import cv2
import numpy

import sys
if (sys.version_info > (3, 0)):
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty

class videoserver(Thread):

    HOST = ''
    PORT = 5001

    def __init__(self, port, send_queue):
        super(videoserver, self).__init__()

        # Define server address
        self.PORT = port

        # Connect with client
        self.wait_connect()

        # Define receiving queue
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
        while 1:
            #print("Drone video server running")
            # Check connection state
            try:
                ready_r, ready_w, in_error = select.select([self.connection,],[self.connection,],[],5)
            except select.error:
                self.connection.shutdown(2)
                self.connection.close()
                print("Connection lost")
                self.wait_connect()
            
            # Send
            if len(ready_w) > 0:
                try:
                    frame = self.send_queue.get_nowait()
                    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
                    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
                    data = numpy.array(imgencode)
                    stringData = data.tostring()
                    self.connection.send( str(len(stringData)).ljust(16));
                    self.connection.send( stringData );
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