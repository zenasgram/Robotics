#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for running a motor to a target position set by the encoder of another motor.
#
# Hardware: Connect EV3 or NXT motors to the BrickPi3 motor ports A and D. Make sure that the BrickPi3 is running on a 9v power supply.
#
# Results:  When you run this program, motor A will run to match the position of motor D. Manually rotate motor D, and motor A will follow.

# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers

# Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP = brickpi3.BrickPi3()

try:
    try:
        BP.offset_motor_encoder(
            BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))  # reset encoder A
        BP.offset_motor_encoder(
            BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))  # reset encoder D
    except IOError as error:
        print(error)

    BP.set_motor_power(BP.PORT_B, BP.MOTOR_FLOAT)    # float motor D
    # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
    BP.set_motor_limits(BP.PORT_A, 50, 200)
    while True:
        # Each of the following BP.get_motor_encoder functions returns the encoder value.
        try:
            target = BP.get_motor_encoder(
                BP.PORT_A)     # read motor D's position
        except IOError as error:
            print(error)

        # set the target speed for motor A in Degrees Per Second
        BP.set_motor_position(BP.PORT_B, target)

        print(("Motor B Target Degrees Per Second: %d" % target),
              "  Motor B Status: ", BP.get_motor_status(BP.PORT_B))

        time.sleep(0.02)
# except the program gets interrupted by Ctrl+C on the keyboard.
except KeyboardInterrupt:
    # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
    BP.reset_all()
