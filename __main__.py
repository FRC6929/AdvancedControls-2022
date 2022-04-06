import sys
import threading
import time
import serial
from networktables import NetworkTables
from playsound import playsound

import logging

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    print("Specifie ip et com")
    exit(0)

ip = sys.argv[1]

ser = serial.Serial("COM3", 9600, timeout=0)

cond = threading.Condition()
notified = [False]

last_palert = 0
palert = False

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()
        pass
    pass

def clear_left(x):
    global ser
    ser.write(b'ABCDEF' + x)

def onValueSwitch(source, key, value, isNew):
    global palert
    if key == 'Mode':
        if value == 'Shooter':
            ser.write(b'h')
            ser.write(b'I')
            playsound('sons/shooter.mp3')
        elif value == 'Elevateur':
            ser.write(b'H')
            ser.write(b'i')
            playsound('sons/elevator.mp3')
    elif key == 'AlertPression':
        if value == True:
            palert = True
            playsound('sons/palert.mp3')
            last_palert = time.time()
        else:
            palert = False
    elif key == 'shooter_set':
        if sd.getString("Mode","jsp") == "Shooter":
            if value == 'lvl1_av':
                clear_left(b'd')
                playsound('sons/lvl1_av.mp3')
                pass
            elif value == 'lvl1_arr':
                clear_left(b'a')
                playsound('sons/lvl1_arr.mp3')
                pass
            elif value == 'lvl2_av':
                clear_left(b'c')
                playsound('sons/lvl2_av.mp3')
                pass
            elif value == 'lvl2_arr':
                clear_left(b'b')
                playsound('sons/lvl2_arr.mp3')
                pass
            elif value == 'intake':
                clear_left(b'e')
                playsound('sons/intake.mp3')
                pass
    elif key == 'Bras':
        if value == 'fixe':
            clear_left(b­'d')
            playsound('sons/bras_fixe.mp3')
        elif value == 'mobile':
            clear_left(b'e')
            playsound('sons/bras_mobile.mp3')

NetworkTables.initialize(server=ip)

sd = NetworkTables.getTable("SmartDashboard")
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

playsound('sons/jingle.mp3',block=False)

with cond:
    #playsound('sons/attente_conn.mp3')
    print("Attente")
    if not notified[0]:
        cond.wait()

print("Connectee")
playsound('sons/conn.mp3')

sd.addEntryListener(onValueSwitch)

i = 0
while True:
    if palert and (time.time() - last_palert) >= 1:
        print('palert')
        last_palert = time.time()
        playsound('sons/palert2.mp3',block=True)
        pass
    time.sleep(1)

print('DECONNECTER')
ser.close()