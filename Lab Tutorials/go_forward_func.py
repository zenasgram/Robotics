# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers


def main():
    # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
    BP = brickpi3.BrickPi3()

    # change this:
    targetA = -4830
    targetB = -4832

    try:
        try:
                # reset encoder
            BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
        except IOError as error:
            print(error)

            # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
        BP.set_motor_limits(BP.PORT_A, 50, 200)
        BP.set_motor_limits(BP.PORT_B, 50, 200)

        # set_position
        BP.set_motor_position(BP.PORT_B, targetB)
        BP.set_motor_position(BP.PORT_A, targetA)

        print(("Motor B Target Degrees Per Second: %d" % targetB),
              "  Motor B Status: ", BP.get_motor_status(BP.PORT_B))

        time.sleep(0.02)

    except KeyboardInterrupt:
            # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        BP.reset_all()


if __name__ == '__main__':
    main()
