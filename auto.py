import bt
import time
import sys
import pygame as pg

pg.init()
pg.mixer.init()

def play(file):
    pg.mixer.load(file)
    pg.mixer.play()
    pg.event.wait()

print(sys.argv)

play('app/static/audio/init.mp3')

start = time.time()
devices = bt.getDevices()
while time.time() - start < 15:
    for device in list(devices.keys()):
        bt.connect(devices[device])
    if bt.getConnected():
        play('app/static/audio/connected.mp3')
        break
bt.advertise()