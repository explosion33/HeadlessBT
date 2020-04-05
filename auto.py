import bt
import time
from playsound import playsound

playsound('app/static/audio/init.mp3')

start = time.time()
devices = bt.getDevices()
while time.time() - start < 15:
    for device in list(devices.keys()):
        bt.connect(devices[device])
    if bt.getConnected():
        playsound('app/static/audio/connected.mp3')
        break
bt.advertise()