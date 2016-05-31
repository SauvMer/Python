from threading import Thread

class QueueTerm(Thread):
    def __init__(self, queue):
        super(QueueTerm, self).__init__()
        self.queue = queue
        self.running = True

    def run(self):
        while self.running:
            msg = input("Enter string to add in queue:\n")
            self.queue.put(msg)

    def end(self):
        self.running = False