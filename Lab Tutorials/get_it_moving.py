# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers

# Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP = brickpi3.BrickPi3()

try:
    BP.set_motor_power(BP.PORT_A, 50)
    BP.set_motor_power(BP.PORT_B, 50)
    while(True):
        print(BP.get_motor_encoder(BP.PORT_A))
except KeyboardInterrupt:
    # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
    BP.reset_all()
