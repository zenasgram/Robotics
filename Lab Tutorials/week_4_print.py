# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
import math
import random

scale = 13
trans = 100


class canvas:

    height = 0
    width = 0

    def print_square(self):
        lines = [(trans, trans, trans, self.height + trans),
                 (trans, trans, self.width+trans, trans),
                 (trans, self.height+trans, self.width+trans, self.height+trans),
                 (self.width+trans, trans, self.width+trans, self.height+trans)
                 ]
        print("drawLine:" + str(lines[0]))
        print("drawLine:" + str(lines[1]))
        print("drawLine:" + str(lines[2]))
        print("drawLine:" + str(lines[3]))

    def __init__(self, height_in, width_in):
        self.height = height_in*scale
        self.width = width_in*scale
        self.print_square()

    def print_particles(self, particles_in):
        print("drawParticles: " + str(particles_in))


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


def forward(dist, particles):
    for i in range(100):
        e = random.gauss(0, 0.05)
        particles[i][0] = particles[i][0] + \
            (dist+e)*math.cos(math.radians(particles[i][2]))
        particles[i][1] = particles[i][1] + \
            (dist+e)*math.sin(math.radians(particles[i][2]))
        f = random.gauss(0, 0.5)
        particles[i][2] = particles[i][2] + f


def rotate(degrees, particles):
    for i in range(100):
        g = random.gauss(0, 0.4)
        particles[i][2] = particles[i][2] + degrees + g


def main():
    # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
    BP = brickpi3.BrickPi3()
    time.sleep(0.02)
    try:
        # BP.set_motor_dps(BP.PORT_A, -300)
        # BP.set_motor_dps(BP.PORT_B, -300)
        # maintain_dist(BP, 30)

        # reset_sonar_sensor(BP)
        # turn_sonar_sensor(BP, "front")
        # turn_sonar_sensor(BP, "right")
        # turn_sonar_sensor(BP, "left")
        # turn_sonar_sensor(BP, "back")
        # turn_sonar_sensor(BP, "front")
        c1 = canvas(40, 40)
        my_particles = [[0, 0, 0] for i in range(100)]
        display_parts = []
        tuple_list = []
        for i in range(4):
            for j in range(4):
                forward(10, my_particles)
                display_parts.extend(my_particles)
                for i in display_parts:
                    x_val = (i[0]+7.7)*scale
                    y_val = (i[1]+47.7)*scale
                    my_tuple = (x_val, y_val, i[2])
                    tuple_list.append(my_tuple)
                c1.print_particles(tuple_list)
                time.sleep(0.5)
            rotate(-90, my_particles)

        #tuple_list = []
     #   for i in display_parts:
      #      x_val = (i[0])*scale
      #      y_val = (i[1])*scale
      #      my_tuple = (x_val,y_val,i[2])
      #      tuple_list.append(my_tuple)

      #  c1.print_particles(tuple_list)

        #tests = [(0, 100), (0, 500), (0, 1000), (0, 1500), (0, 2000), (0, 2500)]

        tests = [(0, 100), (0, 500), (0, 1000),
                 (0, 1500), (0, 2000), (0, 2500)]

        exit

    except KeyboardInterrupt:
            # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        BP.reset_all()


if __name__ == '__main__':
    main()
