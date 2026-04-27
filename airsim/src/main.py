import airsim
import sys
import termios
import tty
import time

# conectar al simulador
client = airsim.MultirotorClient()
client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)

print("Controles:")
print("w/s: subir/bajar")
print("a/d: giroizq/girodercha")
print("i/k: izq/derecha")
print("q: salir")

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

client.takeoffAsync().join()

velocity = 2

while True:
    key = get_key()

    if key == 'q':
        break

    elif key == 'w':
        client.moveByVelocityAsync(0, 0, -velocity, 1)

    elif key == 's':
        client.moveByVelocityAsync(0, 0, velocity, 1)

    elif key == 'a':
        client.moveByVelocityAsync(-velocity, 0, 0, 1)

    elif key == 'd':
        client.moveByVelocityAsync(velocity, 0, 0, 1)

    elif key == 'i':
        client.moveByVelocityAsync(0, velocity, 0, 1)

    elif key == 'k':
        client.moveByVelocityAsync(0, -velocity, 0, 1)

client.landAsync().join()
client.armDisarm(False)
client.enableApiControl(False)
