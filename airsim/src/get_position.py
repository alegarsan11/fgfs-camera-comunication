import airsim
import sys
import termios
import tty
import time

client2 = airsim.VehicleClient()
client2.confirmConnection()

pose = client2.simGetVehiclePose()
print("x={}, y={}, z={}".format(pose.position.x_val, pose.position.y_val, pose.position.z_val))