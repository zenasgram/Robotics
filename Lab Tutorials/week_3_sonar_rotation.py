# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
from _robot_class import *


def main():
    # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
    BP = Robot()
    time.sleep(0.02)
    try:
        BP.reset_sonar_sensor()
        BP.turn_sonar_direction(BP, "front")
        BP.turn_sonar_direction(BP, "right")
        BP.turn_sonar_direction(BP, "left")
        BP.turn_sonar_direction(BP, "back")
        BP.turn_sonar_direction(BP, "front")
        exit

    except KeyboardInterrupt:
            # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        BP.reset_all()


if __name__ == '__main__':
    main()
