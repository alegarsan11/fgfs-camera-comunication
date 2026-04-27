import airsim
import sys
import termios
import tty
import time


client = airsim.MultirotorClient()
print(client)
client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)


client.takeoffAsync().join()
client.moveToPositionAsync(-10, 10, -10, 5).join()