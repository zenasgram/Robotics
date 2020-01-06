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
        BP.set_motor_dps(BP.PORT_A, -300)
        BP.set_motor_dps(BP.PORT_B, -300)
        BP.maintain_distance(BP, 30)
        exit

    except KeyboardInterrupt:
        BP.reset_all()


if __name__ == '__main__':
    main()
