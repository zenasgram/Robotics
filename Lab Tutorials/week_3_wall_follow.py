# use python 3 syntax but make it compatible with python 2
# from __future__ import print_function
# from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers

from _robot_class import *
from _canvas_class import *


def main():
    BP = Robot()
    try:
        BP.reset_sonar_sensor()
        BP.follow_wall(20, 'left', 200)

        BP.go_straight_cm(40)

        test_cases = [
            (0, 0, 0),
            (2, 0, 2),
            (0, 2, 0),
            (4, 5, 0),
            (8, 1, 4)]

        c1 = Canvas(10, 10)
        c1.print_particles(particles_in)
        exit

    except KeyboardInterrupt:
        BP.reset_all()


if __name__ == '__main__':
    main()
