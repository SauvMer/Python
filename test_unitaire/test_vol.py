from dronekit import connect, Command, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

vehicle = connect('/dev/ttyACM0', wait_ready=True)

vehicle.home_location = vehicle.location.global_frame

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print( "Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print( " Waiting for vehicle to initialise...")
        time.sleep(1)

    print( "Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print( "Waiting for arming...")
        time.sleep(1)

    print( "Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    # after Vehicle.simple_takeoff will execute immediately).
    while True:
        print( " Altitude: ", vehicle.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print( "Reached target altitude")
            break
        time.sleep(1)

def arm():
	print( "Basic pre-arm checks")
	# Don't try to arm until autopilot is ready
	while not vehicle.is_armable:
		print( " Waiting for vehicle to initialise...")
		time.sleep(1)

	print( "Arming motors")
	# Copter should arm in GUIDED mode
	vehicle.mode    = VehicleMode("GUIDED")
	vehicle.armed   = True

	# Confirm vehicle armed before attempting to take off
	while not vehicle.armed:
		print( "Waiting for arming...")
		time.sleep(1)
	print('Armed')
# TAKEOFF

#arm_and_takeoff(7)

#arm()

# SPEED PARAMETERS
vehicle.airspeed = 0.7

# Set groundspeed using attribute
vehicle.groundspeed = 2

'''
# SIMPLE GO TO
a_location = LocationGlobalRelative(48.418111, -4.473340, 7) # (-4.47, 48.418)
vehicle.simple_goto(a_location, groundspeed=0.7)
time.sleep(30)
vehicle.mode    = VehicleMode("RTL")
'''


# http://ardupilot.org/planner/docs/common-mavlink-mission-command-messages-mav_cmd.html

# Get commands object from Vehicle.
cmds = vehicle.commands

# Call clear() on Vehicle.commands and upload the command to the vehicle.
cmds.clear()
cmds.upload()

# Get the set of commands from the vehicle
cmds.download()
cmds.wait_ready()

# Create and add commands
cmd1=Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 48.418111, -4.473340, 7)
cmd2=Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 48.418111, -4.473340, 7)
cmd22=Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 48.417995, -4.473628, 7)
cmd3=Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 48.417958, -4.473451, 7)
cmd4=Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 48.417958, -4.473451, 0)
cmds.add(cmd1)
cmds.add(cmd2)
cmds.add(cmd22)
cmds.add(cmd3)
cmds.add(cmd4)
cmds.upload() # Send commands


arm_and_takeoff(7)

vehicle.commands.next = 0

vehicle.mode    = VehicleMode("AUTO")
i=0
while vehicle.commands.next<6:
    time.sleep(1)
    print("Command: %s"%(vehicle.commands.next))
    print("Altitude: %f"%(vehicle.location.global_relative_frame.alt))
    i=i+1



vehicle.close()
