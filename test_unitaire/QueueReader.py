from threading import Thread
from queue import Empty
from time import sleep

class QueueReader(Thread):
    def __init__(self, queue):
        super(QueueReader, self).__init__()
        self.queue = queue
        self.running = True

    def run(self):
        while self.running:
            try:
                msg = self.queue.get_nowait()
                print("Message: %s\n"%msg)
            except Empty:
                pass
            sleep(1)

    def end(self):
        self.running = False