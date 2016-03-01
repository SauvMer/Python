from link import *
from time import sleep
from sys import argv
from ihm import *
from queue import Queue
from threading import Thread

class Base:
    i = True
    def __init__(self, addr, port, queue):
        self.sender = Sender(addr, port)
        self.receiv = Receiv(addr, port+1, self)
        self.queue = queue

    def run(self):
        self.receiv.start()
        '''while 1:
            #msg = input("Message:")
            #self.sender.send_text(msg)
            pass'''

    def stop(self):
        self.sender.send_text("STOP")
        self.receiv.stop = True
        self.sender.sock.close()

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
            self.queue.put("GPS"+gps_string)
        else:
            print("Data received: %s"%data)

if __name__ == "__main__":
    queue = Queue()

    base =Base(argv[1], int(argv[2]), queue)
    print("Base initialized")
    base.run()
    ihm = IHM(base, queue)

    ihm.fenetre.mainloop()
    base.stop()
