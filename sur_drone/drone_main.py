import sys

if (sys.version_info > (3, 0)):
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty

from sys import argv
from time import sleep, time
import platform

from dronekit import connect, Command, VehicleMode
from pymavlink import mavutil

from drone_server import *
from drone_servervideo import videoserver
from drone_detection import *

class Drone:

    def __init__(self, port):
        self.running = True

        # Initialize server
        self.rece_queue = Queue()
        self.send_queue = Queue()
        self.server = server(port, self.rece_queue, self.send_queue)

        # Initialize perception device
        self.dete_queue = Queue()
        self.video_queue = Queue()
        self.detector = Detector(self.dete_queue, self.video_queue)
        self.videoserver = videoserver(port+1, self.video_queue)

        # Initialize vehicle
        #self.vehicle = connect('/dev/ttyACM0', wait_ready=True)
        self.vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)
        #self.vehicle.home_location = self.vehicle.location.global_frame
        self.vehicle.airspeed = 1.2
        self.vehicle.groundspeed = 2
        self.vehicle.commands.clear()

        # Initialize waypoint
        self.waypoints = []

        # Initialize time variable
        self.last_gps = time()

    def run(self):
        # Stating threads
        self.server.start()
        self.videoserver.start()
        self.detector.start()

        while self.running:

            # Send GPS
            if time()-self.last_gps>3:
                #print "Current Waypoint: %s" % self.vehicle.commands.next
                self.last_gps = time()
                pos = self.get_gps()
                self.send_queue.put("GPS" + str(pos[0]) + ";" + str(pos[1]))

            # Reading receiving queue
            try:
                msg = self.rece_queue.get_nowait()
                self.parse_server(msg)
            except Empty:
                pass

            # Reading detection queue
            try:
                msg = self.dete_queue.get_nowait()
                self.parse_detection(msg)
            except Empty:
                pass
        self.server.running = False

    def stop(self):
        print("Stopping process...")
        self.vehicle.close()

    # ------------ PARSING -------------- #
    def parse_server(self, message):

        # 
        print("Message received: %s"%message)

        # Parsing
        if(message.startswith("STOP")):
            self.stop()
        elif(message.startswith("CLEARWAY")):
            self.stop_mission()
        elif(message.startswith("SIMPLETAKEOFF")):
            self.arm_and_takeoff(7)
        elif(message.startswith("ADDWAY")):
            wp = stringtowaypoint(message[6:])
            if wp is not None:
                self.waypoints.append(wp)
        elif(message.startswith("LAND")):
            self.land()
        elif(message.startswith("GO")):
            self.start_mission()
        elif(message.startswith("END")):
            self.detector.running = False
            self.running = False
            self.vehicle.close()

    def parse_detection(self, message):
        if(message.startswith("DETECT")):
            pos = self.get_gps()
            self.send_queue.put("DETECT"+str(pos[0]) + ";" + str(pos[1]))
            print("Victim detected")

    def get_gps(self):
        return [self.vehicle.location.global_frame.lat, self.vehicle.location.global_frame.lon]


    # ---------- FLIGHT COMMANDS ------------ #
    def arm_and_takeoff(self, aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """
        print( "Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        while not self.vehicle.is_armable:
            print( " Waiting for vehicle to initialise...")
            sleep(1)

        print( "Arming motors")
        # Copter should arm in GUIDED mode
        self.vehicle.mode    = VehicleMode("GUIDED")
        self.vehicle.armed   = True

        # Confirm vehicle armed before attempting to take off
        while not self.vehicle.armed:
            print( "Waiting for arming...")
            sleep(1)

        print( "Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        # after Vehicle.simple_takeoff will execute immediately).
        while True:
            print( " Altitude: ", self.vehicle.location.global_relative_frame.alt)
            #Break and return from function just below target altitude.
            if self.vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
                print( "Reached target altitude")
                break
            sleep(1)

    def start_mission(self, height=7):
        if len(self.waypoints) != 0:
            # Initialize commands
            self.vehicle.commands.clear()
            self.vehicle.commands.upload()
            self.vehicle.commands.download()
            self.vehicle.commands.wait_ready()

            # Send waypoints
            for wp in self.waypoints:
                cmd=Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, wp[0], wp[1], height)
                self.vehicle.commands.add(cmd)
            self.vehicle.commands.upload()

            # Take off
            self.arm_and_takeoff(height)

            # Start autonomous flight
            self.vehicle.commands.next = 0
            self.vehicle.mode    = VehicleMode("AUTO")

    def stop_mission(self):
        self.vehicle.commands.clear()
        self.vehicle.commands.upload()

    def land(self):
        self.vehicle.mode = VehicleMode("LAND")

def stringtowaypoint(str):
    coord = str.split(';')
    if len(coord) == 2:
        return [float(coord[0]), float(coord[1])]
    else:
        return None


if __name__ == "__main__":
    drone = Drone(int(argv[1]))
    print("Drone initialized")
    drone.run()
