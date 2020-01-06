from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers


def go_straight_cm(robot_in, distance_in):  # distance_in (cm)

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
    robot_in.set_motor_limits(robot_in.PORT_A, 50, 200)
    robot_in.set_motor_limits(robot_in.PORT_B, 50, 200)

    # set_position
    robot_in.set_motor_position(robot_in.PORT_B, targetB)
    robot_in.set_motor_position(robot_in.PORT_A, targetA)

    while robot_in.get_motor_encoder(robot_in.PORT_A) > targetA and robot_in.get_motor_encoder(robot_in.PORT_B) > targetB:
        print(("Robot target distance: %d" % distance_in),
              "  Motor B Status: ", robot_in.get_motor_status(robot_in.PORT_B),
              "  Motor A Status: ", robot_in.get_motor_status(robot_in.PORT_A))

        time.sleep(0.02)

    return


def rotate(robot_in, degrees):

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
    robot_in.set_motor_limits(robot_in.PORT_A, 50, 200)
    robot_in.set_motor_limits(robot_in.PORT_B, 50, 200)

    # set_position
    robot_in.set_motor_position(robot_in.PORT_B, targetB)
    robot_in.set_motor_position(robot_in.PORT_A, targetA)

    while robot_in.get_motor_encoder(robot_in.PORT_A) > targetA and robot_in.get_motor_encoder(robot_in.PORT_B) < targetB:
        print(("Robot target degrees: %d" % degrees),
              "  Motor B Status: ", robot_in.get_motor_status(robot_in.PORT_B),
              "  Motor A Status: ", robot_in.get_motor_status(robot_in.PORT_A))
        time.sleep(0.02)

    return


def maintain_dist(robot_in, target_distance):
    robot_in.set_sensor_type(
        robot_in.PORT_1, robot_in.SENSOR_TYPE.NXT_ULTRASONIC)
    time.sleep(0.1)  # in case calibration lag

    kp = 30
    dist_list = []
    while True:
        dist_list.append(robot_in.get_sensor(robot_in.PORT_1))
        if len(dist_list) >= 5:
            dist_list.pop(0)
            sorted_list = sorted(dist_list)
            med_val = sorted_list[2]
        else:
            med_val = dist_list[-1]

        buffer = 2
        if(abs(target_distance - med_val) < buffer):
            target_dps = 0
        else:
            target_dps = robot_in.get_motor_status(
                robot_in.PORT_A)[3] + kp * (target_distance - med_val)

        # threshold
        if target_dps > 500:
            target_dps = 500
        if target_dps < -500:
            target_dps = -500

        robot_in.set_motor_dps(robot_in.PORT_A, target_dps)
        robot_in.set_motor_dps(robot_in.PORT_B, target_dps)
        time.sleep(0.05)
        print(robot_in.get_motor_status(
            robot_in.PORT_A)[3])
