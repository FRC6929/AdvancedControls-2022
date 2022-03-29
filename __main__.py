#!/usr/bin/env python3
import sys
import time
from networktables import NetworkTables

import logging

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    print("Specifie ip")
    exit(0)

ip = sys.argv[1]

NetworkTables.initialize(server=ip)

sd = NetworkTables.getTable("SmartDashboard")

i = 0
while True:
    print("robotTime:", sd.getNumber("robotTime", -1))

    sd.putNumber("dsTime", i)
    time.sleep(1)
    i += 1