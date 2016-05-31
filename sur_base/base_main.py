from queue import Queue
from sys import argv
from time import sleep

from base_ihm import *
from base_client import *
from base_clientvideo import *

class Base:

    def __init__(self, addr, port):

        # Initialize client
        self.rece_queue = Queue()
        self.send_queue = Queue()
        self.video_queue = Queue(1)
        self.client = client(addr, port, self.rece_queue, self.send_queue)
        sleep(1)
        self.videoclient = videoclient(addr, port+1, self.video_queue)

        # Initialize ihm
        self.ihm = IHM(self.rece_queue, self.send_queue, self.video_queue)

    def run(self):
        print("Client started")
        self.client.start()
        self.videoclient.start()
        print("IHM started")
        self.ihm.fenetre.mainloop()

    def stop(self):
        print("Stopping process...")
        self.client.end()
        self.videoclient.end()

if __name__ == "__main__":
    base =Base(argv[1], int(argv[2]))
    base.run()

    # IHM LOOP

    base.stop()
