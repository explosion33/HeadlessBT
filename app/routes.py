from flask import render_template, flash, redirect, request, url_for
from app import app
import os
import bt
import subprocess
import time

process = None

def checkProcess(process):
    x = process.poll()
    if x != None:
        print("process ended")
    else:
        s.enter(1, 1, checkProcess, (process,))

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

#main page plus random key handles transfers
@app.route('/')
def index():
    return redirect(url_for("bluetooth"))

@app.route("/bt", defaults={"on": "0"})
@app.route('/bt<on>')
def bluetooth(on):
    global process

    devices = bt.getDevices()
    #devices = {'EthanPhone': 'F0:A3:5A:7B:A4:19', "Bill's IIIIphone": 'F0:A3:5A:7B:A4:19'} #fake data for Windows testing
    c = bt.getConnected()
    #c =  {'Name': 'EthanPhone', 'Type': 'phone'}

    d = list(devices.keys())

    if on == "1":
        process = subprocess.Popen(["python3",app.config["ROOT"] + "bt.py", app.config["ROOT"]])
    if on == "0":
        if process:
            process.kill()

        try:
            os.remove(app.config["ROOT"] + "app/static/stopPairing.txt")
        except:
            pass

    return render_template("bluetooth.html", devices=d, connected=c, on=on)
@app.route('/remove/<device>')
def remove(device):
    devices = bt.getDevices()

    print("removing", device)

    MAC = devices[device]
    bt.remove(MAC)

    return redirect(url_for("bluetooth"))

@app.route('/disconnect')
def disconnect():
    bt.disconnect()
    return redirect(url_for("bluetooth"))

