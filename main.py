from app import app
import subprocess


if __name__ == '__main__':
    process = subprocess.Popen(["python3","/home/pi/flask/auto.py"])
    app.run(host="0.0.0.0", port=app.config["PORT"])