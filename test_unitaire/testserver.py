import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Wireless import clientserver

from time import sleep
from sys import argv
from queue import Queue, Empty

server_queue = Queue()
ser = clientserver.server(int(argv[1]), server_queue)
ser.start()
print("Server running...")
msg = ''
while not 'exit' in msg:
    sleep(1)
    try:
        msg = server_queue.get_nowait()
        print(msg)
    except Empty:
            pass

print("Closing server")
ser.end()