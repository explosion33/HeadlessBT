import bt
import time

start = time.time()
devices = bt.getDevices()
while time.time() - start < 15:
    for device in devices.keys():
        bt.connect(devices[device])