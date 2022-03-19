# HeadlessBT
a headless bluetooth audio and gpio manager for RPI

## UPDATE
on newer versions of raspbian (raspbian desktop) a screen reader prompt will play continiously

kill the process with ```sudo -eaf | grep wiz```
and kill the process with name ```piwiz```, ```kill <pid>```

then remove the file with
```sudo rm /etc/xdg/autostart/piwiz.desktop```


## Setup
turn on RaspberryPi and run through main setup

Right click on the top menu bar and click ```Add / Remove Panel Items```
then scroll down to bluetooth and select remove

next setup audio streaming

## Audio Setup

```
sudo apt-get update
```
```
sudo apt-get install bluez pulseaudio-module-bluetooth python-gobject python-gobject-2
```
then add user "pi" to the default group
```
sudo usermod -a -G lp pi
```
next enter
```
sudo nano /etc/bluetooth/audio.conf
```
and add ```Enable=Source,Sink,Media,Socket``` to the file
then enter
```
sudo nano /etc/pulse/daemon.conf
```
and add ```resample-method = trivial```
Finally Reboot, ```sudo reboot```

Change the bluetooth adapter name by entering:
```
bluetoothctl
system-alias <Alias Here>
exit
```

check to see if the bluetooth is working buy running

```sudo hciconfig hci0 piscan```

the device with the alias should appear under your bluetooth section

if the the device does not show up on an iphone go to a text to hex converter and convert the name you want to show up into hex

for example: ```Car System``` is ```4361722053797374656d```

the max character limit for the hex is 22

if the hex does not reach 22 you need to pad the end with 0's

```4361722053797374656d``` has only 20 characters so you make it ```4361722053797374656d00```

then enter ```sudo /bin/hciconfig hci0 inqdata "0c09[hex here]020a00091002006b1d460217050d03001801180e110c1115110b1100"``` and add your hex code where it says hex here (remove the parenthesis)

this should make it discoverable

Steps adapted from [this](https://www.raspberrypi.org/forums/viewtopic.php?t=68779) guide

ensure audio stream works then procees to download the flask app.

navigate to the home directory and run the command

```git clone https://www.github.com/explosion33/headlessBT flask```

If you changed the install location, modify the config file and update the root

run ```sudo python3 /home/pi/flask/main.py``` and ensure everything works properly. Proceed to WAN setup

## WAN Setup

Run ```sudo apt install dnsmasq hostapd```

then

```
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
```

open ```sudo nano /etc/dhcpcd.conf```

at the bottom enter

```
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```

save and then type

```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
```

open ```sudo nano /etc/dnsmasq.conf```

then type

```
interface=wlan0      # Use the require wireless interface - usually wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
```

start the dnsmasq ```sudo systemctl start dnsmasq```

configure access point

open ```sudo nano /etc/hostapd/hostapd.conf```

enter and change ssid, and password

```
interface=wlan0
driver=nl80211
ssid=NameOfNetwork
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=8CHARPASSPHRASE
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

any wrong typing here will cause the WAN to fail

enter ```sudo nano /etc/default/hostapd```

find the line ```#DAEMON_CONF``` and replace it with ```DAEMON_CONF="/etc/hostapd/hostapd.conf"```

start hostapd

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```

open the wifi browser and ensure you can connect to the network
You will now also be able to SSH into the machine again

Steps adapted from [this](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md) guide


## Run on startup

create a new task in the ```/etc/init.d``` directory
```sudo nano /etc/init.d/startFlask```

enter the following into the file

```
#! /bin/sh
# /etc/init.d/startFlask
### BEGIN INIT INFO
# Provides:          main.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO
 
case "$1" in
  start)
    echo "Starting flask"
    # run application you want to start
    sudo python3 /home/pi/flask/main.py &
    ;;
  stop)
    echo "Stopping flask"
    # kill application you want to stop
    killall python
    ;;
  *)
    echo "Usage: /etc/init.d/startFlask{start|stop}"
    exit 1
    ;;
esac
 
exit 0
```

save the file

run ```sudo chmod 755 /etc/init.d/startFlask``` to give it permissions

run ```sudo update-rc.d startFlask defaults``` to add it to startup
