#final

# use python 3 syntax but make it compatible with python 2
# from __future__ import print_function
# from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers

from _final_robot_class import *
from _final_canvas_class import *
from _final_place_rec_bits import *


def print_test():

    wall_corners=[[0,0],[0,168],[84,168],[84,126],[84,210],[168,210],[168,84],[210,84],[210,0]]
    #wall_corners=[[0,0],[0,40],[40,40],[40,0]]

    CV = canvas(wall_corners)
    CV.print_canvas()

    test_point = [(0,0,0),
                (20,20,0),
                (20,0,0),
                (0,20,0),
                (0,40,0),
                (40,40,0),
                (40,0,0),
                (20,20,0),
                (0,168,0),
                (84,168,0),
                (84,126,0),
                (84,210,0),
                (168,210,0),
                (168,84,0),
                (210,84,0),
                (210,0,0)
                ]
    CV.print_particles(test_point)

    return


def test_square(BP):
    for i in range(4):
        for i in range(4):
            BP.go_straight_cm(10)
            time.sleep(0.5)

        BP.turn(90)
        time.sleep(0.5)

    return

def test_waypoint(BP):
    #while True:
     #   x=float(input("X value"))
      #  y=float(input("Y value"))
       # BP.navigateToWaypoint(x,y)
        #time.sleep(1)

    point_list = [[0,0],[0,168],[84,168],[84,126],[84,210],[168,210],[168,84],[210,84],[210,0]]
    for point in point_list:
        BP.navigateToWaypoint(point[0]/100, point[1]/100)
        time.sleep(1)

    return

def test_sonar(BP):
    while True:
        time.sleep(0.5)
        print (BP.check_sonar_dist('front'))


def test_blocking_straight(BP):
    for i in range(5):
        BP.go_straight_cm(20)

def test_turn(BP):
    for i in range(8):
        BP.turn(90)
        time.sleep(0.5)
        
def test_straight(BP):
    BP.go_straight_cm(210)

def test_blocking_turn(BP):
    for i in range(4):
        BP.turn(90)

def test_monte_carlo(BP):

    BP.turn_sonar_direction("front")
    #point_list = [[180,30],[180,54],[138,54],[138,168],[114,168],[114,84],[84,84],[84,30]]
    point_list = [[104,30],[124,30],[144,30],[164,30],[180,30],
[180,42],[180,54],
[160,54],[150,54],
[138,54],
[138,74],[138,94],[138,114],[138,134],[138,168],[126,168],
[114,168],
[114,148],[114,128],[114,108],
[114,84],
[84,84],[84,64],[84, 50],
[84,30]]
    #point_list = [[50, 30], [60, 10]]

    BP.initialize_position(84,30, 0)
    for point in point_list:
        BP.navigateToWaypointSonar(point[0]/100, point[1]/100)

    return

def test_sonar_sampling(BP):
    
   # signatures = SignatureContainer(5);
    learn_location(BP,0,90)

    return


def test_sonar_turning(BP):
    
   # signatures = SignatureContainer(5);
    BP.turn_sonar_degrees(-180)
    #BP.turn_sonar_degrees(-180)
    #BP.turn_sonar_degrees(-165)
   # time.sleep(7)
   # BP.turn_sonar_degrees(-45)
   # time.sleep(6)
   # BP.turn_sonar_degrees(-60)
   # time.sleep(3)
   # BP.turn_sonar_degrees(-61)
   # time.sleep(2)
    #time.sleep(3)
   # BP.turn_sonar_degrees(0)
   # time.sleep(5)
    
    

    return

def test_signatures(BP):
    signatures = SignatureContainer(5);
    print("ANGLE DIFFERENCE:", find_angle(signatures.read(0), signatures.read(1)))
    
def test_obj_detection(BP, first_degree, last_degree, some_list):
    sig_size = math.floor((last_degree-first_degree)/bin_size)
    #print("sig:",signatures.read(1,sig_size).sig)
    point1 = find_one_object(signatures.read(0,sig_size).sig, some_list, BP.current_x, BP.current_y, first_degree)


#diretion refers to the wall we want to reference    
#ensure direction is either 0, -90, 90, -180 --> front, right, left, back   
def make_bot_perpendicular(BP, direction):
        
    #BP.turn_sonar_degrees(direction)
    
    if(direction == "front"):
        upper=30
        lower=-30 
        
    elif(direction == "back"):
        upper=150
        lower=-150 
        
    elif(direction == "left"):
        upper=120
        lower=60 
    
    elif(direction == "right"):
        upper=-60
        lower=-120
        
    sig = learn_location_runtime(BP,lower,upper) #generates a signature of range 40 degrees 
    sig_size = math.floor(abs(upper-lower)/bin_size) 
    
    print(sig)
    print(sig_size)
    
    #(min_dist,  angle_offset)
    offset_info = find_min_x(sig)
    k=1.3
    if(direction == "front"):
        BP.turn(-offset_info[1]*k)
    elif(direction == "back"):
        BP.turn(-offset_info[1]*k)
    elif(direction == "left"):
        BP.turn(-offset_info[1]*k)
    elif(direction == "right"):
        BP.turn(-offset_info[1]*k)

    
def return_to_waypoint_sonar(BP):
    
    make_bot_perpendicular(BP,0)
    make_bot_perpendicular(BP,-90) 
    BP.navigateToWaypoint(0.84, 0.3,0)
    make_bot_perpendicular(BP,0)
    make_bot_perpendicular(BP,-90)
    
    while(BP.check_sonar_dist_degrees(0) > 30):
        BP.model.set_motor_dps(BP.model.PORT_A,-100)
        BP.model.set_motor_dps(BP.model.PORT_B,-100) 
    
    BP.model.set_motor_dps(BP.model.PORT_A,0)
    BP.model.set_motor_dps(BP.model.PORT_B,0) 
    
    while(BP.check_sonar_dist_degrees(0) < 30):
        BP.model.set_motor_dps(BP.model.PORT_A,100)
        BP.model.set_motor_dps(BP.model.PORT_B,100) 
    
    BP.set_motor_dps(BP.model.PORT_A,0)
    BP.set_motor_dps(BP.model.PORT_B,0) 
      
    
    

    
    
  #  print("point1:",point1)
   # print("point2:",point2)
   # print("point3:",point3)
    
 #   test_sonar_turning(BP)
  #  time.sleep(3)
  #  time.sleep(3)
    
#    BP.navigateToWaypoint(point1[0]/100, point1[1]/100,1)
#    BP.navigateToWaypoint(1.2, 0.5,0)
    
  #  time.sleep(4)
#    BP.navigateToWaypoint(point2[0]/100, point2[1]/100,1)
#    BP.navigateToWaypoint(1.14, 0.84,0)
  #  time.sleep(4)
#    BP.navigateToWaypoint(point3[0]/100, point3[1]/100,1)
#    BP.navigateToWaypoint(0.84, 0.30,0)

def test_sonar(BP):
    BP.turn_sonar_degrees(90)
    print(BP.current_sonar_theta)
    BP.turn_sonar_degrees(180)
    print(BP.current_sonar_theta)
    BP.turn_sonar_degrees(-90)
    print(BP.current_sonar_theta)
    BP.turn_sonar_degrees(-180)
    print(BP.current_sonar_theta)
    BP.turn_sonar_degrees(0)
    print(BP.current_sonar_theta)
    BP.turn(90)
    print(BP.current_theta)
    
def first_waypoint_move(BP):

    sex_bomb = learn_location_runtime(BP,-150,-90)
    obj1 = find_one_object(signatures.read(0,60).sig, sex_bomb, BP.current_x, BP.current_y,BP.current_theta, -150)
    print(obj1)
    time.sleep(1)
    sex_bomb = learn_location_runtime(BP,-70,-10)
    obj2 = find_one_object(signatures.read(1,100).sig, sex_bomb, BP.current_x, BP.current_y,BP.current_theta, -60)
    print(obj2)
    time.sleep(1)
    sex_bomb = learn_location_runtime(BP,10,90)
    obj3 = find_one_object(signatures.read(2,80).sig, sex_bomb, BP.current_x, BP.current_y,BP.current_theta, 10)
    print(obj3)
    time.sleep(1)
    
    return [obj1,obj2,obj3]
    #x_y = find_one_object(first_loc, second_loc, 84, 30, -70)

   # time.sleep(4)
    
def bumping_time(BP,obj1,obj2,obj3):
    
    BP.navigateToWaypoint(obj1[0]/100, obj1[1]/100, 1)   
    
    BP.navigateToWaypoint(1.2, 0.5,0)
    
    BP.navigateToWaypoint(obj2[0]/100, obj2[1]/100, 1)  
    
    BP.navigateToWaypoint(1.2, 0.5,0)
    BP.navigateToWaypoint(0.7, 0.5,0)
    
    BP.navigateToWaypoint(obj3[0]/100, obj3[1]/100, 1) 

    
def approach_wall_sonar(BP, distance_from_wall):

    while(BP.check_sonar_dist_degrees(0) > distance_from_wall+3):
        print("sonar cm: ",BP.check_sonar_dist_degrees(0))
        k = BP.check_sonar_dist_degrees(0) - distance_from_wall
        BP.model.set_motor_dps(BP.model.PORT_A,-(14*k+200))
        BP.model.set_motor_dps(BP.model.PORT_B,-(14*k+200)) 
        time.sleep(0.005)
    BP.model.set_motor_dps(BP.model.PORT_A,0)
    BP.model.set_motor_dps(BP.model.PORT_B,0)
    
    
def away_wall_sonar(BP, distance_from_wall):

    while(BP.check_sonar_dist_degrees(-180) < distance_from_wall-3):
        k =  distance_from_wall -BP.check_sonar_dist_degrees(-180)
        print("k:", k)
        BP.model.set_motor_dps(BP.model.PORT_A,-(14*k+150))
        BP.model.set_motor_dps(BP.model.PORT_B,-(14*k+150))
        time.sleep(0.005)
    
    BP.model.set_motor_dps(BP.model.PORT_A,0)
    BP.model.set_motor_dps(BP.model.PORT_B,0)


    

def learn_with_waypoints(BP):
    
    BP.navigateToWaypoint(1.1, 0.45,0)#used to be: 1.1
    BP.navigateToWaypoint(1.2, 0.45,0)#used to be: 1.2
    learn_location(BP,-35,35)

    BP.navigateToWaypoint(1.2, 1.0,0)
    learn_location(BP,-35,35)
    
    BP.navigateToWaypoint(0.42, 0.75,0)
    BP.navigateToWaypoint(0.42, 0.85,0)
    learn_location(BP,-30,30)
    
    #BP.navigateToWaypoint(0.84, 0.3,0)

def run_with_waypoints(BP):
    BP.turn_sonar_degrees_unblocked(-35)
    BP.navigateToWaypoint(1.1, 0.45,0)#used to be: 1.1
    
    BP.navigateToWaypoint(1.2, 0.45,0)#used to be: 1.2
    
    sig = learn_location_runtime(BP,-35,35)
   # print("sig1:",sig)
    x_y = find_one_object(signatures.read(0,80).sig, sig, BP.current_x, BP.current_y,BP.current_theta, -35, "foo1.png")
    BP.navigateToWaypoint(x_y[0]/100, x_y[1]/100, 1) 
    BP.turn_sonar_degrees_unblocked(-35)
    BP.navigateToWaypoint(1.2, 1.0,0)
    sig = learn_location_runtime(BP,-35,35)
   # print("sig2:",sig)
    x_y = find_one_object(signatures.read(1,80).sig, sig, BP.current_x, BP.current_y,BP.current_theta, -35, "foo2.png")
    BP.navigateToWaypoint(x_y[0]/100, x_y[1]/100, 1) 
    BP.turn_sonar_degrees_unblocked(-30)
    BP.navigateToWaypoint(0.42, 0.75,0)
    BP.navigateToWaypoint(0.42, 0.85,0)
    
   # BP.model.set_motor_position(BP.model.PORT_B, -200) #SUPER HARD CODED FIX
   # BP.model.set_motor_position(BP.model.PORT_A, -200)
    #make_bot_perpendicular(BP, "left")
    sig = learn_location_runtime(BP,-30,30)
    print("sig3:",sig)
    x_y = find_one_object(signatures.read(2,80).sig, sig, BP.current_x, BP.current_y,BP.current_theta, -30, "foo3.png")
    BP.navigateToWaypoint(x_y[0]/100, x_y[1]/100, 1) 
    
    BP.navigateToWaypoint(0.42, 0.75,0)
    
    approach_wall_sonar(BP, 29)
    BP.turn_sonar_degrees_unblocked(-180)
    BP.turn(90)
    away_wall_sonar(BP, 81)
    BP.turn_sonar_degrees_unblocked(0)
    BP.turn(-90)
    approach_wall_sonar(BP, 29)
    
   # return_to_waypoint_sonar(BP)

    
def main():
    BP = Robot()
  #  time.sleep(0.2)
    
    #learn_with_waypoints(BP)
    run_with_waypoints(BP)
    
    
    #test_sonar_turning(BP)
    #test_turn(BP)
    #test_turn(BP)
    #BP.go_straight_cm_w_bump()
    
    #make_bot_perpendicular(BP, "back")
    #time.sleep(3)

    
   # test_straight(BP)
  #  BP.go_straight_cm_w_bump()

   # time.sleep(5)
    #print("FIX IT")
   # test_turn(BP)

    #make_bot_perpendicular(BP,90)
  #  print ("Initial theta:", BP.current_theta)
    #BP.turn(90)
    #BP.turn_sonar_degrees(90)
    
 #   print ("Final theta:", BP.current_theta)
    #learn_with_waypoints(BP)
    
    
    
   # run_with_waypoints(BP)
  #  BP = brickpi3.BrickPi3()
    #characterize_location(BP, ls)
    #print_test()
    #test_waypoint(BP)
    #test_monte_carlo(BP)
    #test_sonar(BP)
    #test_straight(BP)
    #time.sleep(3)

    #print("Done napping")
    #test_sonar_turning(BP)
        
    #BP.navigateToWaypoint(0.84, 0.35,0)
   # print("DONE")
    #time.sleep(4)
#    BP.turn(90)
#    time.sleep(1)
    
    #BP.navigateToWaypoint(1.4, 0.9,0)
    #BP.navigateToWaypoint(1.4, 0.3,0)
    #BP.navigateToWaypoint(0.84, 0.3,0)
#    time.sleep(3)
    #test_sonar_sampling(BP)
    #time.sleep(3)
    #test_sonar_sampling(BP)
    
    #test_sonar_turning(BP)
   # print("GOGOGOG")
    #test_signatures(BP)
   # time.sleep(2)
    #print(signatures.read(0,21).sig)
    #test_obj_detection(BP, 0,90)
#    time.sleep(2)
#    test_sonar_turning(BP)
    #test_sonar(BP)
    
    #find_all_object()
 #   BP.navigateToWaypoint(0.84, 0.9,0)
#   learn_location(BP,-150,-90)
 #   learn_location(BP,-150,-90)
 #   learn_location(BP,-150,-90)
    
 #   learn_location(BP,-70,-10)
 #   learn_location(BP,-70,-10)
 #   learn_location(BP,-70,-10)
   # learn_with_waypoints(BP)
    #BP.turn_sonar_degrees(90)
    #BP.turn_sonar_degrees(180)
  # BP.turn_sonar_degrees(90)
 #   BP.turn_sonar_degrees(45)
 #   BP.turn_sonar_degrees(180)
 #   BP.turn_sonar_degrees(0)
 #   learn_location(BP,10,90)
 #   learn_location(BP,10,90)
 #   learn_location(BP,10,90)
    
   # BP.navigateToWaypoint(0.84, 0.9,0)
   # objects = first_waypoint_move(BP)
   # bumping_time(BP,objects[0],objects[1],objects[2])
   # return_to_waypoint_sonar(BP)
    #test_obj_detection(BP, 0, 90, runtime_list)
    #make_bot_perpendicular(BP, 0)
    #for i in range(180,-180,-1):
    #print(BP.check_sonar_dist_degrees(180))
    #print(BP.check_sonar_dist_degrees(170))
    #print(BP.check_sonar_dist_degrees(-170))  
        #print (BP.model.get_sensor(BP.model.PORT_1))
    #sig = learn_location_runtime(BP,-20,20) #generates a signature of range 40 degrees 

    
    BP.reset_all()
                     
if __name__ == '__main__':
    main()

