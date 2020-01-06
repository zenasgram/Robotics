# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
import math
import random

from _canvas_class import *


class Robot:
    def __init__(self):
        print("robot object initialize")
        self.model = brickpi3.BrickPi3()
        self.canvas_ = canvas(40, 40)
        self.current_x = 0
        self.current_y = 0
        self.current_theta = 0
        self.particles = [[0, 0, 0] for i in range(100)]
        self.canvas_.print_square()



# --------------trivial function---------------------------------------

    def check_stop(self, port_in, threshold_in=1):  # return true if stop
        if abs(self.model.get_motor_status(port_in)[3]) < threshold_in:
            return True
        else:
            return False

    def reset_motor_encoder(self):
        try:
            # reset encoder
            self.model.offset_motor_encoder(
                self.model.PORT_A, self.model.get_motor_encoder(self.model.PORT_A))
            self.model.offset_motor_encoder(
                self.model.PORT_B, self.model.get_motor_encoder(self.model.PORT_B))
        except IOError as error:
            print(error)

    def reset_all(self):
        self.model.reset_all()
        return

# --------------robot motion control-----------------------------------

    def go_straight_cm(self, distance_in):  # distance_in (cm)
        self.forward_particle_update(distance_in)
        targetA = distance_in/40 * -830
        targetB = distance_in/40 * -832

        self.reset_motor_encoder()

        # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
        self.model.set_motor_limits(self.model.PORT_A, 70, 400)
        self.model.set_motor_limits(self.model.PORT_B, 70, 400)

        # set_position
        self.model.set_motor_position(self.model.PORT_B, targetB)
        self.model.set_motor_position(self.model.PORT_A, targetA)

        # blocking
        while self.model.get_motor_encoder(self.model.PORT_A) < targetA and self.model.get_motor_encoder(self.model.PORT_B) < targetB:
            if self.check_stop(self.model.PORT_A) and self.check_stop(self.model.PORT_B):
                break

            print(("Robot target distance: %d" % distance_in),
                  "  Motor B Status: ", self.model.get_motor_status(
                      self.model.PORT_B),
                  "  Motor A Status: ", self.model.get_motor_status(self.model.PORT_A))
            time.sleep(0.02)

        self.update_x_y_theta()
        return

    def turn(self, degrees):  # direction 1 means left
        self.rotate_particle_update(degrees)
        targetA = degrees/90 * -284
        targetB = degrees/90 * 284

        self.reset_motor_encoder()

        # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
        self.model.set_motor_limits(self.model.PORT_A, 50, 200)
        self.model.set_motor_limits(self.model.PORT_B, 50, 200)

        # set_position
        self.model.set_motor_position(self.model.PORT_B, targetB)
        self.model.set_motor_position(self.model.PORT_A, targetA)

        if(degrees > 0):

            while self.model.get_motor_encoder(self.model.PORT_A) > targetA and self.model.get_motor_encoder(self.model.PORT_B) < targetB:
                print(("Robot target degrees: %d" % degrees),
                      "  Motor B Status: ", self.model.get_motor_status(
                          self.model.PORT_B),
                      "  Motor A Status: ", self.model.get_motor_status(self.model.PORT_A))
                time.sleep(0.02)
                if self.check_stop(self.model.PORT_A) and self.check_stop(self.model.PORT_B):
                    break

        else:
            while self.model.get_motor_encoder(self.model.PORT_A) < targetA and self.model.get_motor_encoder(self.model.PORT_B) > targetB:
                print(("Robot target degrees: %d" % degrees),
                      "  Motor B Status: ", self.model.get_motor_status(
                          self.model.PORT_B),
                      "  Motor A Status: ", self.model.get_motor_status(self.model.PORT_A))
                time.sleep(0.02)
                if self.check_stop(self.model.PORT_A) and self.check_stop(self.model.PORT_B):
                    break
        self.update_x_y_theta()
        return

    def navigateToWaypoint(self, x_in, y_in):  # x_in and y_in are in metres
        #converting metres into cm
        y_in = y_in * 100
        x_in = x_in * 100

        x_diff = x_in-abs(self.current_x)
        y_diff = y_in-abs(self.current_y)

        if x_diff is 0:
            desired_theta = 90
        else:
            desired_theta = math.degrees(math.atan(y_diff/x_diff))

        turn_degree = -(desired_theta - self.current_theta)

        print("x_diff: ", x_diff)
        print("y_diff: ", y_diff)
        print("turn_degree: ", turn_degree)


        self.turn(turn_degree)
        time.sleep(1)
        tangent_distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
        print("tangent_distance : ", tangent_distance)
        self.go_straight_cm(tangent_distance)
        time.sleep(1)
        self.turn(-turn_degree)

        return

    def bump(self, turn_direc):
        self.go_straight_cm(self.model, -5)
        print("POINT 1")
        self.turn(self.model, 3, turn_direc)

        return

    def maintain_dist(self, target_distance):
        self.model.set_sensor_type(
            self.model.PORT_1, self.model.SENSOR_TYPE.NXT_ULTRASONIC)
        time.sleep(0.1)  # in case calibration lag

        kp = 30
        dist_list = []
        while True:
            dist_list.append(self.model.get_sensor(self.model.PORT_1))
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
                target_dps = self.model.get_motor_status(
                    self.model.PORT_A)[3] + kp * (target_distance - med_val)

            # threshold
            if target_dps > 500:
                target_dps = 500
            if target_dps < -500:
                target_dps = -500

            self.model.set_motor_dps(self.model.PORT_A, target_dps)
            self.model.set_motor_dps(self.model.PORT_B, target_dps)
            time.sleep(0.05)
            print(self.model.get_motor_status(
                self.model.PORT_A)[3])

    def follow_wall(self, target_distance, wall_direction, target_dps):
        self.turn_sonar_sensor(wall_direction)
        self.model.set_sensor_type(
            self.model.PORT_1, self.model.SENSOR_TYPE.NXT_ULTRASONIC)
        time.sleep(0.1)  # in case calibration lag

        # might to move this into a separate function(return the )
        Kp = 10
        dist_list = []
        while True:
            dist_list.append(self.model.get_sensor(self.model.PORT_1))
            if len(dist_list) >= 5:
                dist_list.pop(0)
                sorted_list = sorted(dist_list)
                med_val = sorted_list[2]
            else:
                med_val = dist_list[-1]

            # stop jerking motion by manipulating target_dps
            buffer = 2
            # if(abs(target_distance - med_val) < buffer):
            #     left_dps = target_dps
            #     right_dps = target_dps
            #
            # else:
            # current_distance = self.model.get_motor_status(self.model.PORT_A)[3]

            if wall_direction is "left":
                left_dps = target_dps + 0.5 * Kp * (target_distance - med_val)
                right_dps = target_dps - 0.5 * Kp * (target_distance - med_val)
            elif wall_direction is "right":
                left_dps = target_dps - 0.5 * Kp * (target_distance - med_val)
                right_dps = target_dps + 0.5 * Kp * (target_distance - med_val)

            if left_dps > 500:
                left_dps = 500
            if left_dps < -500:
                left_dps = -500
            if right_dps > 500:
                right_dps = 500
            if right_dps < -500:
                right_dps = -500

            # left only

            self.model.set_motor_dps(self.model.PORT_A, -left_dps)
            self.model.set_motor_dps(self.model.PORT_B, -right_dps)
            time.sleep(0.05)
        return


# --------------sensor control-----------------------------------------

    def reset_sonar_sensor(self):
        try:
            self.model.set_motor_power(self.model.PORT_D, -5)
            time.sleep(0.3)
            self.model.set_motor_power(self.model.PORT_D, 10)
            time.sleep(0.5)
            while self.model.get_motor_status(self.model.PORT_D)[3] >= 1:
                time.sleep(0.02)
            self.model.set_motor_power(self.model.PORT_D, 0)
            # if(self.model.get_motor_status)
            self.model.offset_motor_encoder(
                self.model.PORT_D, self.model.get_motor_encoder(self.model.PORT_D))
            time.sleep(0.5)

        except IOError as error:
            print(error)

    # direction_in = (right, left, back, front)
    def turn_sonar_direction(self, direction_in):
        if (direction_in is "right"):
            self.reset_sonar_sensor()
        else:
            dict_ = {"left": -375,
                     "back": -531,
                     "front": -210}

            self.model.set_motor_limits(self.model.PORT_D, 50, 200)
            self.model.set_motor_position(
                self.model.PORT_D, dict_[direction_in])

            time.sleep(0.5)

            # blocking
            while abs(self.model.get_motor_status(self.model.PORT_D)[3]) > 0.1:
                time.sleep(0.05)

                # print(self.model.get_motor_status(self.model.PORT_D))
        time.sleep(0.5)
        return

# --------------particle filtering and location estimates-----------------------------------------

    def forward_particle_update(self,dist):
        for i in range(100):
            e = random.gauss(0, 0.05)
            self.particles[i][0] = self.particles[i][0] + \
                (dist+e)*math.cos(math.radians(self.particles[i][2]))
            self.particles[i][1] = self.particles[i][1] + \
                (dist+e)*math.sin(math.radians(self.particles[i][2]))
            f = random.gauss(0, 0.5)
            self.particles[i][2] = self.particles[i][2] + f
        self.canvas_.print_particles(self.particles)

    def rotate_particle_update(self,degrees):
        for i in range(100):
            g = random.gauss(0, 0.4)
            self.particles[i][2] = self.particles[i][2] + degrees + g
        self.canvas_.print_particles(self.particles)

    def update_x_y_theta(self):
        dummy_x=0
        dummy_y=0
        dummy_theta=0
        for i in self.particles:
            dummy_x = dummy_x + i[0]
            dummy_y = dummy_y + i[1]
            dummy_theta = dummy_theta + i[2]
        self.current_x = dummy_x/100
        self.current_y = dummy_y/100
        self.current_theta = dummy_theta/100
