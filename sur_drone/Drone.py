from random import uniform
from threading import Thread
from time import sleep

class Command:
    def __init__(self, a,z,e,r,t,y,u,i,o,p,q,s,d,f):
        # Do nothing
        pass

class Vehicle:
    def __init__(self):
        self.mode = None
        self.armed = True
        self.commands = Commands()
        self.location = Location()
        self.location.global_frame = Coordinate(48.417995, -4.473628)
        self.location.global_frame.start()

    def close(self):
        self.location.global_frame.boo = False

class Location:
    def __init__(self):
        self.global_frame = None

class Coordinate(Thread):
    def __init__(self, lat, lon):
        super(Coordinate, self).__init__()
        self.boo = True
        self.lat = lat
        self.lon = lon

    def run(self):
        while self.boo:
            #print("Drone running")
            self.lat += 0.0001*uniform(-1, 1)
            self.lon += 0.0001*uniform(-1, 1)
            sleep(1)


class VehicleMode:
    def __init__(self, mode):
        pass

def connect(port, wait_ready=True):
    return Vehicle()

class Commands:
    def __init__(self):
        self.list = []
        self.count = 0

    def add(self, command):
        self.list.append(command)
        self.count += 1

    def wait_ready(self):
        pass

    def download(self):
        pass

    def upload(self):
        self.list = []
        self.count = 0

    def clear(self):
        self.list = []

class Mavlink:
    MAV_FRAME_GLOBAL_RELATIVE_ALT = 0
    MAV_CMD_NAV_WAYPOINT = 0

class mavutil:
    mavlink = Mavlink()

