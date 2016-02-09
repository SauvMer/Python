import socket
import sys

class client:

    def __init__(self, adress, port):

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address = (adress, port)
        print('connecting to %s port %s' % self.server_address)
        self.sock.connect(self.server_address)
        print('connected')

    def close(self):
        self.sendText('close')
        self.sock.close()

    def sendText(self, text):
        self.sock.sendall(text.encode())

    def receiveText(self):
        data = ''
        data += self.sock.recv(256).decode()
        return data

    def getCaptors(self):
        print('sending command')
        self.sendText('captor')
        print('waiting for response')
        data = self.receiveText()
        return data


if __name__=='__main__':
    cli = client(sys.argv[1], int(sys.argv[2]))
    captors = cli.getCaptors()
    print(captors)
    cli.close()