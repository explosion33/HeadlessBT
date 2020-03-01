import subprocess

def runCmd(cmd):
    """
    runCmd (cmd): runs a command in the shell (can use a heredoc)\n
    cmd : str containing a command\n
    returns : the console output from running the command
    """
    x = subprocess.check_output(cmd, shell=True)
    x = x.decode("utf-8")
    return x

def getDevices():
    """
    getDevices () : gets a dictionary of all connected devices and their mac address\n
    returns : {"name": "MAC",}
    """

    cmd = '''bluetoothctl <<EOF
    devices
    exit
    EOF
    '''
    out = repr(runCmd(cmd))
    devices = {}

    while out.find("Device") != -1:
        x = out.find("Device")
        MAC = out[x+7:x+7+17]

        name = ""
        for i in range(len(out)-x-25):
            p = out[i+x+25]
            if p + out[i+x+26] == "\\n":
                break
            name += p
        devices[name] = MAC
        out = out[x+7+16::]

    return devices

def getNewDevices(deviceList):
    """
    getNewDevices(deviceList) : gets the devices that have been added since the previous list\n
    deviceList : a list obtained through getDevices that is older by atleast a tick\n
    returns : {"name": "MAC",}
    """
    d = getDevices()

    devices = {}

    if d != deviceList:
        dK = list(d.keys())
        dK2 = list(deviceList.keys())

        for key in dK:
            if key not in dK2:
                devices[key] = d[key]

    return devices

def pair(device):
    """
    remove(device) : pairs a device by Trusting it\n
    device : a string containing the mac address of the device\n
    returns : console log during command
    """

    cmd1 = '''bluetoothctl <<EOF
    trust '''

    cmd2 = '''
    exit
    EOF
    '''

    cmd = cmd1 + str(device) + cmd2
    out = repr(runCmd(cmd))
    return out

def remove(MAC):
    """
    remove(device) : removes a device from the paired bluetooth devices\n
    MAC : a string containing the mac address of the device\n
    returns : console log during command
    """
    cmd1 = '''bluetoothctl <<EOF
    remove '''

    cmd2 = '''
    exit
    EOF
    '''

    cmd = cmd1 + str(MAC) + cmd2
    out = repr(runCmd(cmd))

    return out

def getConnected():
    """
    getConnected() : gets teh currently connected device\n
    returns : {name: "name", "MAC": "MAC", "Type": "type"}
    """

    cmd = '''bluetoothctl <<EOF
    info
    exit
    EOF
    '''
    out = repr(runCmd(cmd))

    print(out)

    device = {}

    x = out.find("Name: ")

    if x >= 0:

        out = out[x+6::]

        name = ""
        for i in range(len(out)):
            c1 = out[i]
            c2 = out[i+1]

            if c1 + c2 == "\\n":
                break
            name += c1

        device["Name"] = name

    if x>=0:

        x = out.find("Icon: ")
        out = out[x+6::]

        icon = ""
        for i in range(len(out)):
            c1 = out[i]
            c2 = out[i+1]

            if c1 + c2 == "\\n":
                break
            icon += c1

        device["Type"] = icon
    
    return device

if "main" in __name__: #if bt is called directly it runs a sctipt to handle incoming pairing requests
    devices = getDevices()
    print(devices)
    while True:
        x = getNewDevices(devices)
        if x:
            print(x)
            k = list(x.keys())
            out = pair(x[k[0]])
            print(out)
            break
        else:
            print(x, devices)