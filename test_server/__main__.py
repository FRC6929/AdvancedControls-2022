import time
from networktables import NetworkTables

# To see messages from networktables, you must setup logging
import logging

logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

#time.sleep(1)

i = 0
while True:
    txt = input(">")

    if txt == 'mode_shooter':
        sd.putString('Mode','Shooter')
        pass
    elif txt == 'mode_elevator':
        sd.putString('Mode','Elevator')
        pass
    elif txt == 'palert_true':
        sd.putBoolean('AlertPression', True)
    elif txt == 'palert_false':
        sd.putBoolean('AlertPression', False)
    elif txt == 'exit' or txt == 'quit':
        exit(0)
    else:
        print('Unknown command')
        pass
