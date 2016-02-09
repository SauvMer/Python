import socket
import sys

class server:

    def __init__(self, adress, port):

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = (adress, port)
        print('starting up on %s port %s' % self.server_address)
        self.sock.bind(self.server_address)

        # Listen for incoming connections
        self.sock.listen(1)

        # Wait for a connection
        print('waiting for a connection')
        self.connection, self.client_address = self.sock.accept()
        print('connected')

    def close(self):
        self.sock.close()

    def sendText(self, text):
        self.connection.sendall(text.encode())

    def receiveText(self):
        data = ''
        data += self.connection.recv(256).decode()
        return data

if __name__=='__main__':
    ser = server(sys.argv[1], int(sys.argv[2]))
    while True:
        command = ser.receiveText()
        print('command: %s'%(command))
        if(command == 'captor'):
            ser.sendText('GPS: lat, lon; Gyro: 1,1,1')
        elif(command == 'close'):
            ser.close()
            break
