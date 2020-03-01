from flask import render_template, flash, redirect, request, url_for
from app import app
import os
import bt

devices = bt.getDevices()

#main page plus random key handles transfers
@app.route('/')
def index():
    return render_template("home.html")

@app.route('/bt')
def bluetooth():
    global devices
    devices = bt.getDevices()
    #devices = {'EthanPhone': 'F0:A3:5A:7B:A4:19', "Bill's IIIIphone": 'F0:A3:5A:7B:A4:19'} #fake data for Windows testing
    c = bt.getConnected()
    #c =  {'Name': 'EthanPhone', 'Type': 'phone'}

    d = list(devices.keys())

    return render_template("bluetooth.html", devices=d, connected=c)
@app.route('/remove/<device>')
def remove(device):
    global devices

    print("removing", device)

    MAC = devices[device]
    bt.remove(MAC)

    return redirect(url_for("bluetooth"))