import sys
import threading
import time
from networktables import NetworkTables
from playsound import playsound

import logging

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    print("Specifie ip")
    exit(0)

ip = sys.argv[1]

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server=ip)

sd = NetworkTables.getTable("SmartDashboard")
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

playsound('sons/jingle.mp3',block=False)

with cond:
    playsound('sons/attente_conn.mp3')
    print("Waiting")
    if not notified[0]:
        cond.wait()

print("Connectee")
playsound('sons/conn.mp3')

i = 0
while True:
    print("robotTime:", sd.getNumber("robotTime", -1))

    sd.putNumber("dsTime", i)
    time.sleep(1)
    i += 1