import subprocess
from time import sleep
from sys import argv

pidserver = subprocess.Popen(args=[
    "gnome-terminal", "--command=python3 testserver.py %s"%argv[1]]).pid
print(pidserver)
sleep(1)
pidclient = subprocess.Popen(args=[
    "gnome-terminal", "--command=python3 testclient.py %s"%argv[1]]).pid
print(pidclient)
