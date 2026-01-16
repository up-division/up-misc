import gpiod
import time
from gpiod.line import Direction, Value

LINE0 = 22 #15
LINE1 = 23 #16
LINE2 = 24 #18
LINE3 = 27 #13
TOGGLE = 1
LOOP = 0

with gpiod.request_lines(
    "/dev/gpiochip1",
    consumer="gpio 22-27, 23-24 testing",
    config={
        LINE0: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        ),
        LINE1: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        ),
        LINE2: gpiod.LineSettings(
            direction=Direction.INPUT
        ),
        LINE3: gpiod.LineSettings(
            direction=Direction.INPUT
        )    
    },
) as request:
    while True:
        if TOGGLE == 1:
            request.set_value(LINE0, Value.INACTIVE)
            request.set_value(LINE1, Value.INACTIVE)
            time.sleep(0.1)
            value = request.get_value(LINE3)
            if value != Value.INACTIVE:
                print("{}={} value is incorrect from LINE0".format(LINE3, value))
                break
            value = request.get_value(LINE2)
            if value != Value.INACTIVE:
                print("{}={} value is incorrect from LINE1".format(LINE2, value))
                break
            TOGGLE = 0
        else:
            request.set_value(LINE0, Value.ACTIVE)
            request.set_value(LINE1, Value.ACTIVE)
            time.sleep(0.1)       
            value = request.get_value(LINE3)
            if value != Value.ACTIVE:
                print("{}={} value is incorrect from LINE0".format(LINE3, value))
                break
            value = request.get_value(LINE2)
            if value != Value.ACTIVE:
                print("{}={} value is incorrect from LINE1".format(LINE2, value))
                break
            TOGGLE = 1
        LOOP+=1    
        print("loop counter {}\r".format(LOOP),end='',flush=True)
        time.sleep(0.1)
