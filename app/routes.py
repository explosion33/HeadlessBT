from flask import render_template, flash, redirect, request, url_for
from app import app
import os

#main page plus random key handles transfers
@app.route('/')
def index():
    return render_template("home.html")
