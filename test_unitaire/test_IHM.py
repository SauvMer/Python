import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from base_ihm import IHM
from queue import Queue
from test_unitaire.QueueTerm import QueueTerm
from test_unitaire.QueueReader import QueueReader

base_queue = Queue()
ihm_queue = Queue()
video_queue = Queue()

base_watcher = QueueReader(base_queue)
ihm_input = QueueTerm(ihm_queue)
base_watcher.start()
ihm_input.start()

ihm = IHM(base_queue, ihm_queue, video_queue)
ihm.fenetre.mainloop()

base_watcher.end()
ihm_input.end()
