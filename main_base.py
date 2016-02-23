from link import *
from time import sleep
from sys import argv

class Base:
    i = True
    def __init__(self, addr, port):
        self.sender = Sender(addr, port)
        self.receiv = Receiv(addr, port+1, self)

    def run(self):
        self.receiv.start()
        while 1:
            #msg = input("Message:")
            #self.sender.send_text(msg)
            pass

    def parse_receiv(self, data):
        if data.startswith("image"):
            if self.i:
                filename = 'result.png'
            else:
                filename = 'result2.png'
            self.i = not self.i
            self.receiv.receiv_image(filename)
        elif data.startswith("GPS"):
            gps_string = data[3:]
            print(gps_string)
        else:
            print("Data received: %s"%data)

if __name__ == "__main__":
    base =Base(argv[1], int(argv[2]))
    print("Base initialized")
    base.run()