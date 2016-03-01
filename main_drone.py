from link import *
from time import sleep
from sys import argv

class Drone:

    def __init__(self, addr, port):
        self.receiv = Receiv(addr, port, self)
        self.sender = Sender(addr, port+1)
        self.waypoints = []

    def run(self):
        self.receiv.start()
        while not self.receiv.stop:
            # IMAGE SENDING
            #self.sender.send_text("image")
            #self.sender.send_image("test.png")
            sleep(2)
            # GPS SENDING
            gps_string = self.get_gps()
            self.sender.send_text("GPS" + gps_string)
            # USER INPUT SENDING
            #msg = input("Message:")
            #self.sender.send_text(msg)

    def stop(self):
        self.receiv.stop = True
        self.sender.sock.close()

    def parse_receiv(self, data):
        print("Data received: %s"%data)
        if(data.startswith("GPS")):
            gps_string = self.get_gps()
            self.sender.send_text("GPS" + gps_string)
        elif(data.startswith("STOP")):
            self.stop()
        elif(data.startswith("ADDWAY")):
            wp = stringtowaypoint(data[6:])
            if wp != None:
                self.waypoints.append(wp)
            print(self.waypoints)

    def get_gps(self):
        #simu
        return gps_file.readline().replace('\n', '')

def stringtowaypoint(str):
    coord = str.split(',')
    if len(coord) == 8:
        return [float(coord[0]), float(coord[1]), float(coord[2]), coord[3],
                float(coord[4]), float(coord[5]), float(coord[6]), coord[7]]
    else:
        return None


if __name__ == "__main__":
    # simu
    gps_file = open("gps.txt", 'r')

    drone = Drone(argv[1], int(argv[2]))
    print("Drone initialized")
    drone.run()