import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Wireless import clientserver
from sys import argv
from queue import Queue

client_queue = Queue()
cli = clientserver.client("localhost", int(argv[1]), client_queue)
cli.start()
print("Client running...")
inp = ''
while not 'exit' in inp:
    inp = input("Enter command (exit to leave)\n")
    cli.send_text(inp)


print("Closing client")
cli.end()