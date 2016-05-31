import socket
import sys, os
from threading import Thread

class Sender:

    def __init__(self, addr, port):
        self.server_addr = ('', port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.server_addr)
        self.sock.bind(self.server_addr)
        print("Listening...")
        self.sock.listen(1)
        print("Establishing...")
        self.connection, self.client_address = self.sock.accept()

    def send_text(self, text):
        self.connection.sendall(text.encode())
        self.connection.recv(256)

    def send_image(self, filename):
        print("Sending image...")
        # Open image file
        file = open(filename, 'rb')
        # Get image size
        size = os.path.getsize(filename)
        # Send image size
        self.send_text(str(size))
        # Send image
        bytes = file.read(1024)
        while len(bytes) != 0:
            self.connection.send(bytes)
            bytes = file.read(1024)
        # Received confirmation
        self.connection.recv(256)
        # Close image file
        file.close()
        print("Image send.")

class Receiv(Thread):

    def __init__(self, addr, port, parent):
        super(Receiv, self).__init__()
        self.server_addr = (addr, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting...")
        self.sock.connect(self.server_addr)
        self.parent = parent
        self.stop = False

    def run(self):
        while not self.stop:
            data = self.receiv_text()
            self.parent.parse_receiv(data)
        self.sock.close()

    def receiv_text(self):
        data = self.sock.recv(256).decode()
        self.sock.sendall("OK".encode())
        return data

    def receiv_image(self, filename):
        print("Receiving image...")
        # Get image size
        size = int(self.receiv_text())
        # Create received image file
        file = open(filename, 'wb+')

        # Receive image
        for i in range(0, int(size/1024)+1):
            bytes = self.sock.recv(1024)
            file.write(bytes)
        # Send confirmation
        self.sock.sendall("OK".encode())
        # Close received image file
        file.close()
        print("Image received.")
