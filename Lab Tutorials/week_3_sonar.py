# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers


# return a tuple of the (left_dps, right_dps)
def turn_while_driving(robot_in, angle_in, straight_dps_in):
    return


def reset_sonar_sensor(robot_in):
    try:
        robot_in.set_motor_power(robot_in.PORT_D, -5)
        time.sleep(0.3)
        robot_in.set_motor_power(robot_in.PORT_D, 10)
        time.sleep(0.5)
        while robot_in.get_motor_status(robot_in.PORT_D)[3] >= 1:
            time.sleep(0.02)
        robot_in.set_motor_power(robot_in.PORT_D, 0)
        # if(robot_in.get_motor_status)
        robot_in.offset_motor_encoder(
            robot_in.PORT_D, robot_in.get_motor_encoder(robot_in.PORT_D))
        time.sleep(0.5)

    except IOError as error:
        print(error)


def turn_sonar_sensor(robot_in, direction_in):
    print("enter: ", direction_in)
    if (direction_in is "right"):
        reset_sonar_sensor(robot_in)
    else:
        dict_ = {"left": -375,
                 "back": -531,
                 "front": -210}

        robot_in.set_motor_limits(robot_in.PORT_D, 50, 200)
        robot_in.set_motor_position(robot_in.PORT_D, dict_[direction_in])

      #  power = robot_in.get_motor_status(robot_in.PORT_D)[1]
      #  prev_power = power
        time.sleep(0.5)
        while abs(robot_in.get_motor_status(robot_in.PORT_D)[3]) > 0.1:
            time.sleep(0.05)
            print(robot_in.get_motor_status(robot_in.PORT_D))

    time.sleep(0.5)
    print("exit: ", direction_in)
    return


# def follow_wall(robot_in, dist_from_wall, current_dps):  # distance_in (cm)
#     robot_in.set_sensor_type(
#         robot_in.PORT_1, robot_in.SENSOR_TYPE.NXT_ULTRASONIC)
#     time.sleep(0.1)  # in case calibration lag
#     kp = 30
#     while True:
#     #     target_dps = current_dps - kp * \
#     #         (dist_from_wall - robot_in.get_sensor(robot_in.PORT_1))
#     #     robot_in.set_motor_dps(robot_in.PORT_B, target_dps)
#     #     time.sleep(0.02)
#     return


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


def main():
    # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
    BP = brickpi3.BrickPi3()
    time.sleep(0.02)
    try:
        # BP.set_motor_dps(BP.PORT_A, -300)
        # BP.set_motor_dps(BP.PORT_B, -300)
        maintain_dist(BP, 30)
      #  reset_sonar_sensor(BP)
       # turn_sonar_sensor(BP, "front")
        turn_sonar_sensor(BP, "right")
        turn_sonar_sensor(BP, "left")
        turn_sonar_sensor(BP, "back")
        turn_sonar_sensor(BP, "front")
        exit

    except KeyboardInterrupt:
            # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        BP.reset_all()


if __name__ == '__main__':
    main()
