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
def blueTooth():
    global devices
    devices = bt.getDevices()

    d = list(devices.keys())

    print(devices,d)

    return render_template("bluetooth.html", devives=d)