#new file for final
# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
import math
import random
import numpy as np
from cmath import rect, phase
from math import radians, degrees
from _final_canvas_class import *
#import matplotlib.pyplot as plt

# everything is in cm tho

#TODO:_

#1. tidy up the reset sonar, check sonar, come up with value(dist to origin), test sonar
#2. build function for detection and building the signature
#3. slow speed down as we approach the target, touch sensor
#4.



class Robot:
    
    def __init__(self):
        print("robot object initialize")
        
        #setup
        self.wall_corners=[[0,0],[0,168],[84,168],[84,126],[84,210],[168,210],[168,84],[210,84],[210,0]]
        self.model = brickpi3.BrickPi3()
        self.canvas_ = canvas(self.wall_corners)
        self.model.set_sensor_type(self.model.PORT_1, self.model.SENSOR_TYPE.NXT_ULTRASONIC)
        self.reset_sonar_sensor()
        self.reset_motor_encoder()
        self.model.set_motor_limits(self.model.PORT_A, 100, 200) #left motor
        self.model.set_motor_limits(self.model.PORT_B, 100, 200) #right motor
        self.model.set_motor_limits(self.model.PORT_D, 50, 200) #sonar sensor
        self.model.set_sensor_type(self.model.PORT_4, self.model.SENSOR_TYPE.TOUCH)
        self.model.set_sensor_type(self.model.PORT_2, self.model.SENSOR_TYPE.TOUCH)
        
      #  self.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.TOUCH)
        #canvas and localisation
        self.backwards_cm_amount = 12
        self.current_x = 84
        self.current_y = 30
        self.current_theta = 0
        self.current_sonar_direction = "right"
        self.current_sonar_theta = 0 
        self.particles = [[[84, 30, 0],0] for i in range(100)]
        
        
        #sonar
        self.sonar_current_theta = 0 #relative to robot- front
        
        
        self.debug = False
        
        


    # --------------sonar control-----------------------------------------

    
    #double check
    def reset_sonar_sensor(self):
        try:
            self.model.offset_motor_encoder(self.model.PORT_D, self.model.get_motor_encoder(self.model.PORT_D))

        except IOError as error:
            print(error)
            
            
            
    def print_oneself_loc(self):
        self.canvas_.print_particle((self.current_x, self.current_y, self.current_theta))

            
  

    def check_sonar_dist_degrees(self, degrees_in):
        dist_list = []
        self.turn_sonar_degrees(degrees_in)
        while len(dist_list) < 5:

            try:
                z = self.model.get_sensor(self.model.PORT_1)
                dist_list.append(z)
            except:
                print("sensor_error")

            time.sleep(0.0005)

        sorted_list=sorted(dist_list)
        med_val = sorted_list[2]
        
        #actual_distance = self.calc_cosine_formula(med_val,8,self.current_sonar_theta)
        
        return med_val
    
    def calc_cosine_formula(self, b,c,angleA):
        answer_squared = b**2 +c**2 +2*b*c*math.cos(math.radians(angleA))
        return math.sqrt(answer_squared)
    
    
    # turn sonar to the desired degree relative to robot, following polar convention
    # 180 <= degrees_in < -180
    # degrees_in is the desired angle, regardless of current degrees_in
    def turn_sonar_degrees(self, degrees_in):
        initial_pos = self.model.get_motor_encoder(self.model.PORT_D)
        #calibration constant
       # k = -672/360
        k = 3400/360
        position = k * degrees_in
        #calibration from sonar position to desired degree turn, NB: -ve sign for counterclockwise rotation

        self.model.set_motor_limits(self.model.PORT_D, 95, 1000)
        self.model.set_motor_position(self.model.PORT_D, position)

        #blocking sonar
        sleep_time = abs(initial_pos- position)/760
        time.sleep(sleep_time +0.001)

        #update current_sonar_theta
        self.current_sonar_theta = math.radians(degrees_in)

        return
        
    def turn_sonar_degrees_unblocked(self, degrees_in):
        initial_pos = self.model.get_motor_encoder(self.model.PORT_D)
        #calibration constant
       # k = -672/360
        k = 3400/360
        position = k * degrees_in
        #calibration from sonar position to desired degree turn, NB: -ve sign for counterclockwise rotation

        self.model.set_motor_limits(self.model.PORT_D, 95, 900)
        self.model.set_motor_position(self.model.PORT_D, position)

        #blocking sonar
      #  sleep_time = abs(initial_pos- position)/740
       # time.sleep(sleep_time +0.001)

        #update current_sonar_theta
        self.current_sonar_theta = math.radians(degrees_in)

        return
        


# --------------robot motion control-----------------------------------


    def go_straight_cm(self, distance_in):  # distance_in (cm)
        # what negate the distance_in
        targetA = distance_in/40 * -886
        targetB = distance_in/40 * -886

        self.reset_motor_encoder()

        # # set_position
        
        self.model.set_motor_limits(self.model.PORT_A, 90, 800)
        self.model.set_motor_limits(self.model.PORT_B, 90, 800)
        
        self.model.set_motor_position(self.model.PORT_B, targetB)
        self.model.set_motor_position(self.model.PORT_A, targetA)

        # blocking
        while self.model.get_motor_encoder(self.model.PORT_A) > targetA+7 and self.model.get_motor_encoder(self.model.PORT_B) > targetB+7:
            time.sleep(0.02)


        self.model.set_motor_dps(self.model.PORT_B, 0)
        self.model.set_motor_dps(self.model.PORT_A, 0)
        time.sleep(0.2)
        
       # self.forward_particle_update(distance_in)
       # self.update_x_y_theta()
        
        self.current_x =  self.current_x + distance_in*math.cos(math.radians(self.current_theta))
        self.current_y =  self.current_y + distance_in*math.sin(math.radians(self.current_theta))
        
        #x_final = x_initial+distance*math.cos(math.radians(theta-90))
        

        return
    
    
    def go_straight_cm_w_bump(self):  # distance_in (cm)
        # what negate the distance_in
  #      targetA = distance_in/40 * -892
  #      targetB = distance_in/40 * -892

        self.reset_motor_encoder()
        
        
        while self.model.get_sensor(self.model.PORT_4)==0 and self.model.get_sensor(self.model.PORT_2)==0:
            
            k = self.check_sonar_dist_degrees(0)
       
            self.model.set_motor_dps(self.model.PORT_A, -17*k)
            self.model.set_motor_dps(self.model.PORT_B, -17*k)
            time.sleep(0.002)
        #print("before loop")

        # blocking
       # while self.model.get_sensor(self.model.PORT_4)==0 and self.model.get_sensor(self.model.PORT_2)==0:
       #     time.sleep(0.008)
            
            
       # print("out of while loop")
        self.model.set_motor_dps(self.model.PORT_A, 0)
        self.model.set_motor_dps(self.model.PORT_B, 0)
       # print("ENCODER A: ",self.model.get_motor_encoder(self.model.PORT_A))
       # print("ENCODER B: ",self.model.get_motor_encoder(self.model.PORT_B))
        time.sleep(0.05)
        
       # self.model.set_motor_position(self.model.PORT_A, -self.model.get_motor_encoder(self.model.PORT_A))
       # self.model.set_motor_position(self.model.PORT_B, -self.model.get_motor_encoder(self.model.PORT_B))
        self.model.set_motor_dps(self.model.PORT_A, 700)
        self.model.set_motor_dps(self.model.PORT_B, 700)
        while self.model.get_motor_encoder(self.model.PORT_A) < 15:
            time.sleep(0.02)
   #         print("MOTOR ENCODER VALUE:",self.model.get_motor_encoder(self.model.PORT_A))
    #    print("Out of reverse while loop!")
        self.model.set_motor_dps(self.model.PORT_A, 0)
        self.model.set_motor_dps(self.model.PORT_B, 0)
        time.sleep(0.2)
     #   self.model.set_motor_dps(self.model.PORT_B, 0)
     #   self.model.set_motor_dps(self.model.PORT_A, 0)
     #   time.sleep(0.2)
        
        
     #   self.model.get_motor_encoder(self.model.PORT_D)
        
     #   self.current_x =  self.current_x + ((-self.model.get_motor_encoder(self.model.PORT_A)/40* 850))*math.cos(math.radians(self.current_theta))
     #   self.current_y =  self.current_y + ((-self.model.get_motor_encoder(self.model.PORT_A)/40* 850))*math.sin(math.radians(self.current_theta))
        
     #   self.go_straight_cm(-10)
        
        return


    
    
    def turn(self, degrees):
        print("Turning")
        #A is the left rotor, while b is right
        #degree positive, turn left
        targetA = degrees/90 * 273
        targetB = degrees/90 * -273
        
        self.reset_motor_encoder()

        self.model.set_motor_limits(self.model.PORT_A, 70, 200)
        self.model.set_motor_limits(self.model.PORT_B, 70, 200)
        
        self.model.set_motor_position(self.model.PORT_B, targetB)
        self.model.set_motor_position(self.model.PORT_A, targetA)

        if(degrees > 0):
            while self.model.get_motor_encoder(self.model.PORT_A) < targetA-5 and self.model.get_motor_encoder(self.model.PORT_B) > targetB+5:
                time.sleep(0.05)

        else:
            while self.model.get_motor_encoder(self.model.PORT_A) > targetA+5 and self.model.get_motor_encoder(self.model.PORT_B) < targetB-5:
                time.sleep(0.05)

        time.sleep(0.2)
       # self.rotate_particle_update(degrees)
      #  self.update_x_y_theta()
        self.current_theta = self.current_theta + degrees
  
        return
    
    
    def navigateToWaypoint(self, x_in, y_in, will_bump):  # x_in and y_in are in metres
        #converting metres into cm
        y_in = y_in * 100
        x_in = x_in * 100

        x_diff = x_in-self.current_x
        y_diff = y_in-self.current_y

        desired_theta = math.degrees(math.atan2(y_diff,x_diff))
        turn_degree = desired_theta - self.current_theta
        
        if(turn_degree > 180):
                turn_degree = turn_degree - 360
        elif ( turn_degree < -180):
                turn_degree = turn_degree + 360

        self.turn(turn_degree)
        print("about to go straight")
        tangent_distance = math.sqrt(x_diff ** 2 + y_diff ** 2)

        if will_bump ==1:
            #print ("with_bump")
            self.go_straight_cm_w_bump()
        else:
            #print ("no_bump")
            self.go_straight_cm(tangent_distance)
            
        self.print_oneself_loc()

        return


    def navigateToWaypointSonar(self, x_in, y_in):  # x_in and y_in are in metres
        # converting metres into cm

        y_in = y_in * 100
        x_in = x_in * 100

        x_diff = x_in-self.current_x
        y_diff = y_in-self.current_y

        desired_theta = math.degrees(math.atan2(y_diff,x_diff))

        turn_degree = desired_theta - self.current_theta
        # print(turn_degree)
        if(turn_degree > 180):
                turn_degree = turn_degree - 360
        elif ( turn_degree < -180):
                turn_degree = turn_degree + 360

        self.turn(turn_degree)

        tangent_distance = math.sqrt(x_diff ** 2 + y_diff ** 2)

        print("BEFORE GOING STRAIGHT")
        self.go_straight_cm(tangent_distance)
        print("AFTER GOING STRAIGHT")
        z = self.check_sonar_dist("front")

        highest_likelihood = 0
        for i in self.particles:
            i[1] = self.calc_likelihood(i[0][0],i[0][1],i[0][2],z)
            if i[1] > highest_likelihood:
                highest_likelihood = i[1]

        self.normalise_resample()

        self.update_x_y_theta()

        return


    
    
    
# --------------particle filtering and location estimates-----------------------------------------

    def forward_particle_update(self, dist):

        for i in range(len(self.particles)):
            e = random.gauss(0, math.sqrt(0.02*dist))
            self.particles[i][0][0] = self.particles[i][0][0] + \
                (dist+e)*math.cos(math.radians(self.particles[i][0][2]))
            self.particles[i][0][1] = self.particles[i][0][1] + \
                (dist+e)*math.sin(math.radians(self.particles[i][0][2]))
            f = random.gauss(0, 0.5)
            self.particles[i][0][2] = self.particles[i][0][2] + f
        self.canvas_.print_particles(self.particles)



    def rotate_particle_update(self, degrees):

        new_p_list = []

        # print("rotate before: ", self.particles)
        for i in self.particles:
            g = random.gauss(0, math.sqrt(0.05 * abs(degrees)))
            # print( "degrees: ", degrees, "self_p: ", i[0][2])
            new_th = i[0][2] + degrees + g
            new_particles = [[i[0][0],i[0][1], new_th], i[1]]

            new_p_list.append(new_particles)

        self.particles = new_p_list
        # print("rotate after: ", self.particles)
        #self.canvas_.print_particles(self.particles)



    def update_x_y_theta(self):


        x_list = [i[0][0] for i in self.particles]
        y_list = [i[0][1] for i in self.particles]
        degree_list = [i[0][2] for i in self.particles]
        self.current_x = sum(x_list)/len(x_list)
        self.current_y = sum(y_list)/len(y_list)
        self.current_theta = self.calc_angle_mean(degree_list)


    def calc_angle_mean(self, angles):
        #CHECK_THIS
        return degrees(phase(sum(rect(1, radians(d)) for d in angles)/len(angles)))

    
    

    def calc_m(self, vertex_A, vertex_B, x, y, theta): #assuming  theta is given as degrees
        numerator = (vertex_B[1]-vertex_A[1])*(vertex_A[0]-x) - (vertex_B[0]-vertex_A[0])*(vertex_A[1]-y)
        denom = (vertex_B[1]-vertex_A[1])*math.cos(math.radians(theta)) - (vertex_B[0]-vertex_A[0])*math.sin(math.radians(theta))
        if denom == 0:
            return -1

        return (numerator/denom)
    
    

    def is_within_bounds(self, vertex_A, vertex_B, point_C):
        max_x = max(vertex_A[0],vertex_B[0])
        min_x = min(vertex_A[0],vertex_B[0])
        max_y = max(vertex_A[1],vertex_B[1])
        min_y = min(vertex_A[1],vertex_B[1])
        if point_C[0] <= max_x and point_C[0] >= min_x and point_C[1] <= max_y and point_C[1] >= min_y:
            return True
        else:
            return False


    def pick_m(self, m_list, wall_corners, x, y, theta):
        #pruning m_list by making sure m must be positive, endpoint lies within wall's ends
        #refactories by getting rid of append, invalid m are penalized with high m,
        #valid_m_list = []

        for i in range(len(m_list)):
            if m_list[i] <=0:
                m_list[i] = 90000000
            else:
                new_x = round(x + m_list[i] * math.cos(math.radians(theta)), 6)
                new_y = round(y + m_list[i] * math.sin(math.radians(theta)), 6)

                if i != len(m_list) - 1: # this check is to ensure array wraps around from last element to first
                    if not self.is_within_bounds(wall_corners[i],wall_corners[i+1],[new_x, new_y]):
                        m_list[i] = 90000000
                else:
                    if not self.is_within_bounds(wall_corners[i],wall_corners[0],[new_x, new_y]):
                        m_list[i] = 90000000

        return min(m_list)
    
    
    

    def calc_likelihood(self, x, y, theta, z):

        m_list = []

        for i in range(len(self.wall_corners)):
            if i!=len(self.wall_corners)-1:
                m_list.append(self.calc_m(self.wall_corners[i],self.wall_corners[i+1], x, y, theta))
            else:
                m_list.append(self.calc_m(self.wall_corners[i],self.wall_corners[0], x, y, theta))


        m = self.pick_m(m_list, self.wall_corners, x, y, theta)
        if (m == 90000000):
            print("ERROR(calc_likelihood): no suitable wall detected")

        likelihood = self.calculate_pdf( z-m , 0, 2.4, 0.005) # +0.1 to make the prediction robust against sonar anomalies

        return likelihood
    
    
    

    def calculate_pdf(self, actual_val, mean, st_dev, offset):
        return math.exp(-((actual_val-mean)**2/(2*st_dev*st_dev))) + offset

    
    
    
    def normalise_resample(self):

        #ensure the sum of all weights = 1
        #might need to figure ways to ditch normalization afterward
        old_weights = np.array([i[1] for i in self.particles])
        normalized_weights = old_weights /old_weights.sum()

        #resampling
        new_particles =[]

        for i in range(len(self.particles)):
            new_particle_index = np.random.choice(range(len(self.particles)), p = normalized_weights)
            # ^ needs index because choice function requires 1D array
            new_particles.append([self.particles[new_particle_index][0], 1/len(self.particles)])

        self.particles = new_particles

        return

    
# --------------trivial function---------------------------------------


    def check_stop(self, port_in, threshold_in = 4):  # return true if stop
        if abs(self.model.get_motor_status(port_in)[3]) < threshold_in:
            return True
        else:
            return False
        
        
    def bump(self):
        
      #  backwards_cm_amount = 12
        self.reset_motor_encoder()
        pos = self.backwards_cm_amount/40 * 850
    #    true_pos_A = pos - self.model.get_motor_encoder(self.model.PORT_A)
        #true_pos_B = pos - self.model.get_motor_encoder(self.model.PORT_B)
       # self.go_straight_cm(backwards_cm_amount)
        self.model.set_motor_position(self.model.PORT_A,pos)
        self.model.set_motor_position(self.model.PORT_B,pos)
        #self.turn(self.model, 3, turn_direc)
       # time.sleep(1.5)
        print("finished with bump")
        return

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
        self.reset_motor_encoder()
        self.model.reset_all()
        return

    def initialize_position(self, x_in, y_in, theta_in):
        self.current_x = x_in
        self.current_y = y_in
        self.current_theta = theta_in
        self.particles = [[[x_in, y_in, theta_in],0.01] for i in range(len(self.particles))]
        self.update_x_y_theta()
        self.canvas_.print_particles(self.particles)
        #self.model.set_sensor_type(self.model.PORT_1, self.model.SENSOR_TYPE.NXT_ULTRASONIC)

        return

