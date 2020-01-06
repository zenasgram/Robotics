# use python 3 syntax but make it compatible with python 2
from __future__ import print_function
from __future__ import division  # ''

import sys
import time     # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers


class canvas:

    def __init__(self, wall_corners_in):
        #self.scale = 13
        self.scale = 2.5
        self.trans = 100
        self.wall_corners = wall_corners_in

        self.margin_top = 100
        self.margin_left = 100

        maxheight = 0
        for i in range(len(self.wall_corners)):
            if self.wall_corners[i][1] > maxheight:
                maxheight =  self.wall_corners[i][1]

        self.height = maxheight*self.scale

        self.print_canvas()
        self.display_parts = []
        self.tuple_list = []


    def flip_point(self, tuple_in):
        # step 1 above, round to get nearest integer
        x_tmp = tuple_in[0]
        y_tmp = tuple_in[1] - self.height/self.scale

        # step 2 above
        y_tmp = -y_tmp

        x_tmp = x_tmp*self.scale + self.margin_left
        y_tmp = y_tmp*self.scale + self.margin_top
        return (x_tmp, y_tmp)


    def print_canvas(self):

        lines = []
        line_tmp = [] #setting up each line to be appended into list

        for i in range(len(self.wall_corners)):

            point_A = self.flip_point(self.wall_corners[i])
            if i != (len(self.wall_corners)-1):
                point_B = self.flip_point(self.wall_corners[i+1])

            #edge case for last element
            if i == len(self.wall_corners)-1:
                line_tmp = (point_A[0], point_A[1], self.flip_point(self.wall_corners[0])[0], self.flip_point(self.wall_corners[0])[1])
                #line_tmp = (self.trans+(self.wall_corners[i][0]*self.scale), self.trans+(self.wall_corners[i][1]*self.scale), self.trans+(self.wall_corners[0][0]*self.scale), self.trans+(self.wall_corners[0][1]*self.scale))

            #spits out line (x1, y1, x2, y2)
            else:
                line_tmp = (point_A[0], point_A[1], point_B[0], point_B[1])
                #line_tmp = (self.trans+(self.wall_corners[i][0]*self.scale), self.trans+(self.wall_corners[i][1]*self.scale), self.trans+(self.wall_corners[i+1][0]*self.scale), self.trans+(self.wall_corners[i+1][1]*self.scale))
            lines.append(line_tmp)


        for i in range(len(lines)):
            print("drawLine:" + str(lines[i]))
    
    
    def print_objects(self, x, y):
        
        
        point = [round(x),round(y)]
        obj = self.flip_point(point);
        
        
        
        line1 = (obj[0]-20, obj[1]-20, obj[0]+20, obj[1]+20)
        line2 = (obj[0]-20, obj[1]+20, obj[0]+20, obj[1]-20) 
        
        print("drawLine:" + str(line1))
        print("drawLine:" + str(line2))
         

    def print_particle(self, particle_in):

        y_val = particle_in[1] - self.height/self.scale
        x_val = particle_in[0]

        # step 2 above
        y_val = -y_val

        x_val = x_val*self.scale + self.margin_left
        y_val = y_val*self.scale + self.margin_top
        my_tuple = (x_val, y_val, particle_in[2])

        display =[]
        display.append(my_tuple)

        print("drawParticles: " + str(display))
        

    def print_particles(self, particles_in):
        # input in cm , output in pixel
        # see above, necessary translation from input to output(display using provided api)
        # 1. move origin to the upper left, eraticating all negative point
        # 2. flip the canvas around the y-axis
        # 3. remember that cm is scaled using self.scale into pixel on screen
        keep_tracked = False;

        # print("size particles_in ", len(particles_in))
        # print("before print x: ", particles_in[0][0][0])
        # print("before print y: ", particles_in[0][0][1])
        for i in particles_in:

            # step 1 above, round to get nearest integer
            y_val = i[0][1] - self.height/self.scale
            x_val = i[0][0]

            # step 2 above
            y_val = -y_val

            x_val = x_val*self.scale + self.margin_left
            y_val = y_val*self.scale + self.margin_top
            my_tuple = (x_val, y_val, i[0][2])

            # step 3 above
            #x_val = (x_val + 7.7)*self.scale
            #y_val = (y_val + 7.7)*self.scale
            #my_tuple = (x_val, y_val, i[2])
            self.tuple_list.append(my_tuple)

        if keep_tracked:
            self.display_parts.extend(self.tuple_list)
        else:
            self.display_parts = self.tuple_list

        display = [(d[0],d[1]) + d[2:] for d in self.display_parts];
        print("particles.size: " + len(display))
        print("drawParticles: " + str(display))
        # print("drawParticles: " + str(self.display_parts))
        # print(self.tuple_list[0])

