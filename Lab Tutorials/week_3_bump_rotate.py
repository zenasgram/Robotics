# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers


def bump(robot_in, turn_direc):
    go_straight(robot_in, -5)
    print("POINT 1")
    turn(robot_in, 3, turn_direc)

    return


def roam_with_detec(robot_in):
    print("About to set motor dps")
    robot_in.set_motor_dps(robot_in.PORT_A, -450)
    robot_in.set_motor_dps(robot_in.PORT_B, -450)
    while(True):
        if robot_in.get_sensor(robot_in.PORT_3):
            turn_direc = 0
            break
        elif robot_in.get_sensor(robot_in.PORT_4):
            turn_direc = 1
            break
        time.sleep(0.02)
    return turn_direc


def go_straight(robot_in, distance_in):  # distance_in (cm)

    targetA = distance_in/40 * -830
    targetB = distance_in/40 * -832

    try:
        # reset encoder
        robot_in.offset_motor_encoder(
            robot_in.PORT_A, robot_in.get_motor_encoder(robot_in.PORT_A))
        robot_in.offset_motor_encoder(
            robot_in.PORT_B, robot_in.get_motor_encoder(robot_in.PORT_B))
    except IOError as error:
        print(error)

        # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
    robot_in.set_motor_limits(robot_in.PORT_A, 70, 400)
    robot_in.set_motor_limits(robot_in.PORT_B, 70, 400)
    print("About to set motor position.")
    # set_position
    robot_in.set_motor_position(robot_in.PORT_B, targetB)
    robot_in.set_motor_position(robot_in.PORT_A, targetA)
    while robot_in.get_motor_encoder(robot_in.PORT_A) < targetA and robot_in.get_motor_encoder(robot_in.PORT_B) < targetB:
        # print(("Robot target distance: %d" % distance_in),
          #    "  Motor B Status: ", robot_in.get_motor_status(robot_in.PORT_B),
        #      "  Motor A Status: ", robot_in.get_motor_status(robot_in.PORT_A))

        time.sleep(0.02)

    return


def turn(robot_in, degrees, direction):

    targetA = degrees/90 * -264
    targetB = degrees/90 * 264
    try:
        # reset encoder
        robot_in.offset_motor_encoder(
            robot_in.PORT_A, robot_in.get_motor_encoder(robot_in.PORT_A))
        robot_in.offset_motor_encoder(
            robot_in.PORT_B, robot_in.get_motor_encoder(robot_in.PORT_B))
    except IOError as error:
        print(error)
        # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
    # set_position
    if(direction):
        robot_in.set_motor_dps(robot_in.PORT_B, -200)
        robot_in.set_motor_dps(robot_in.PORT_A, 200)
    else:
        robot_in.set_motor_dps(robot_in.PORT_B, 200)
        robot_in.set_motor_dps(robot_in.PORT_A, -200)

    while abs(robot_in.get_motor_encoder(robot_in.PORT_A)) < abs(targetA) and abs(robot_in.get_motor_encoder(robot_in.PORT_B)) < abs(targetB):
        #print("I am waiting here")
        # print(("Robot target degrees: %d" % degrees),
         #     "  Motor B Status: ", robot_in.get_motor_status(robot_in.PORT_B),
          #    "  Motor A Status: ", robot_in.get_motor_status(robot_in.PORT_A))

        time.sleep(0.02)
    print("End of turn.")

    time.sleep(0.2)
    return


def main():
    # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
    BP = robot()
    BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.TOUCH)
    BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.TOUCH)
    time.sleep(0.02)
    try:
        while(True):
            direc = roam_with_detec(BP)
            bump(BP, direc)
            print("Ive reached end of while in main.")
    except KeyboardInterrupt:
        BP.reset_all()


if __name__ == '__main__':
    main()
