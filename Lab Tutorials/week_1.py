from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers


def main():
    BP = brickpi3.BrickPi3()
    targetA1 = -830
    targetB1 = -832
    targetA2 = -264
    targetB2 = 264
    try:
        BP.set_motor_limits(BP.PORT_A, 50, 200)
        BP.set_motor_limits(BP.PORT_B, 50, 200)
        for i in range(4):
            try:
                BP.offset_motor_encoder(
                    BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
                BP.offset_motor_encoder(
                    BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            except IOError as error:
                print(error)
            BP.set_motor_position(BP.PORT_B, targetB1)
            BP.set_motor_position(BP.PORT_A, targetA1)

            while BP.get_motor_encoder(BP.PORT_A) > targetA1 and BP.get_motor_encoder(BP.PORT_B) > targetB1:
                time.sleep(0.2)
            try:
                BP.offset_motor_encoder(
                    BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
                BP.offset_motor_encoder(
                    BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            except IOError as error:
                print(error)
            BP.set_motor_position(BP.PORT_B, targetB2)
            BP.set_motor_position(BP.PORT_A, targetA2)
            while BP.get_motor_encoder(BP.PORT_A) > targetA2 and BP.get_motor_encoder(BP.PORT_B) < targetB2:
                time.sleep(0.2)
    except KeyboardInterrupt:
            # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        BP.reset_all()


if __name__ == '__main__':
    main()
