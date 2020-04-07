import bt
import time
import sys
import pygame as pg

time.sleep(7)


pg.init()
pg.mixer.init()

def play(file):
    pg.mixer.music.load(file)
    pg.mixer.music.play()


root = sys.argv[1]

play(root + '/app/static/audio/init.mp3')

start = time.time()
devices = bt.getDevices()
while True:
    while time.time() - start < 15:
        print("searching")
        for device in list(devices.keys()):
            bt.connect(devices[device])
        if bt.getConnected():
            play(root + '/app/static/audio/connected.mp3')
            break
    bt.advertise()
    start = time.time()
    while bt.getConnected():
        print("waiting")