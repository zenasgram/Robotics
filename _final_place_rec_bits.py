#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import os
#from matplotlib import pyplot as plt
from _final_robot_class import *
from _final_canvas_class import *

#variable bin size -> affects histogram resolution. eg. 5 degree iteration
bin_size = 1

# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self):
        self.no_bins = int(360/bin_size)
        self.sig = []

    def print_signature(self):
        for i in range(len(self.sig)):
            print (self.sig[i])

# --------------------- File management class ---------------
class SignatureContainer():
    def __init__(self, size = 10):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];

        # Fills the filenames variable with names like loc_%%.dat
        # where %% are 2 digits (00, 01, 02...) indicating the location number.
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1

        if (n >= self.size):
            return -1;
        else:
            return n;

    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print ("STATUS:  All signature files removed.")
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])

    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)

        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close();

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index,sig_size):
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):

            f = open(filename, 'r')
            for i in range(sig_size):
                s = f.readline()
               # print("i:", i)
               # print("s:",s)
                if (s != ''):
                    ls.sig.append(int(s))
            f.close();
        else:
            print ("WARNING: Signature does not exist.")

        return ls

# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(BP, ls,first_degree, last_degree):
    #print "TODO:    You should implement the function that captures a signature."

    #print("histogram(angles-depth)\n")
    #print("my range",range(math.floor((last_degree - first_degree)/bin_size)))
    for i in range(math.floor((last_degree - first_degree)/bin_size)):
       # print(bin_size)
        #print(i)
        #BP.turn_sonar_degrees(-first_degree-i*bin_size) #rotate by bin_size counterclockwise
        ls.sig.append(BP.check_sonar_dist_degrees(first_degree+i*bin_size))
        
        #ls.sig[i] = random.randint(0, 255)
      #  print("angle: ", i , "depth: ", ls.sig[i])
    print("ls.sig:",ls.sig)
   # BP.turn_sonar_degrees(0)
    BP.turn_sonar_degrees_unblocked(0)
    #reset sonar sensor HERE


    return

# FILL IN: compare two signatures
def compare_signatures(ls1, ls2):
    #REPLACE ALL USES OF LS WITH LS.SIG

    highest_depth = 265
    lowest_depth = 0
    number_of_depth_bins = 40
    depth_bins = np.linspace(lowest_depth, highest_depth, num=number_of_depth_bins)
    depth_counts_1 = [0] * number_of_depth_bins
    depth_counts_2 = [0] * number_of_depth_bins

    #modify both signature to be shift invariant
    for i in range(len(ls1.sig)):
        index = int(np.digitize(ls1.sig[i], depth_bins,right = False))
        #above digitize function could be implemented using:
            # j = 0
            # while ls1.sig[i] < depth_bins:
            #     j++
            # index = j
        depth_counts_1[index] = depth_counts_1[index] + 1

        index = int(np.digitize(ls2.sig[i], depth_bins,right = False))
        depth_counts_2[index] = depth_counts_2[index] + 1

    #compute least square difference between two signature
    dist = 0
    for i in range(number_of_depth_bins):
        dist = dist + (depth_counts_1[i]-depth_counts_2[i])**2

    # print "TODO:    You should implement the function that compares two signatures."
    return dist

# This function characterizes the current location, and stores the obtained
# signature into the next available file.
def learn_location(BP,first_degree, last_degree):
    ls = LocationSignature()
    print ("entering characterize_loc")
    characterize_location(BP,ls,first_degree, last_degree)
    print ("Finished characterize_loc")
    idx = signatures.get_free_index();
    if (idx == -1): # run out of signature files
        print ("\nWARNING:")
        print ("No signature file is available. NOTHING NEW will be learned and stored.")
        print ("Please remove some loc_%%.dat files.\n")
        return

    signatures.save(ls,idx)
    print ("STATUS:  Location " + str(idx) + " learned and saved.")

    
def learn_location_runtime(BP,first_degree, last_degree):
    ls = LocationSignature()
    print ("entering characterize_loc")
    characterize_location(BP,ls,first_degree, last_degree)
    print ("Finished characterize_loc")
    
    return ls.sig


def find_angle(ls1, ls2):
    bestAngle = -1
    bestDist = float("inf")

    #find the one index with lowest_depth
    i = 0
    while i < len(ls1.sig):
        j = 0
        dist = 0
        while j < len(ls1.sig):
            dist += (ls1.sig[j] - ls2.sig[(j+i)%len(ls1.sig)])**2 #modulo 40 make sure we are taking the first 40 values
            j += 1
        if dist < bestDist:
            bestDist = dist
            bestAngle = i
        i += 1

    bestAngle = bestAngle *360 / len(ls1.sig)
    return bestAngle

# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen


def recognize_location(BP):
    ls_obs = LocationSignature();
    characterize_location(BP, ls_obs);
    bestDist = float("inf")
    bestIndex = -1
    threshold = 5000

    # FILL IN: COMPARE ls_read with ls_obs and find the best match
    for idx in range(signatures.size):
        print ("STATUS:  Comparing signature " + str(idx) + " with the observed signature.")
        ls_read = signatures.read(idx);
        dist    = compare_signatures(ls_obs, ls_read)
        print ("Distance between " + str(idx + 1) + " and the observed signature is " + str(dist))
        if dist < threshold and dist < bestDist:
            bestDist = dist
            bestIndex = idx

    if (bestIndex != -1):
        print ("Best location is location " + str(bestIndex + 1))
        angle = findAngle(ls_obs, signatures.read(bestIndex))
        print ("The robot is rotated by " + str(angle) + " degrees")
    else:
        print ("We might be lost...")

# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files().
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.


def find_all_object(sample_sig, current_sig, current_x, current_y):

  #  objA=[]
  #  objB=[]
  #  objC=[]
  #  subtract_list=[]

    #compute difference between signature_without object and signature_with_object
  #  for i in range(len(sample_sig)):
  #      subtract_list.append(sample_sig[i]-current_sig[i])

    #filter noise
  #  for i in range(len(subtract_list)):
  #      if subtract_list[i] < 15:
  #          subtract_list[i]=0
   # plt.scatter(range(len(subtract_list))[60:250],subtract_list[60:250])


   # plt.savefig("foo5.png")

    polA=find_one_object()
    polB=find_one_object(90,270,subtract_list, current_sig)
    polC=find_one_object(270,360,subtract_list, current_sig)

    print(polA)
    print(polB)
    print(polC)

    #objA = polar_to_cartesian(current_x, current_y, polA[0],polA[1])
    #objB = polar_to_cartesian(current_x, current_y, polB[0],polB[1])
    #objC = polar_to_cartesian(current_x, current_y, polC[0],polC[1])

    #update web GUI with cylinders
    wall_corners=[[0,0],[0,168],[84,168],[84,126],[84,210],[168,210],[168,84],[210,84],[210,0]]
    CV = canvas(wall_corners)
    CV.print_objects(objA[0],objA[1])
    CV.print_objects(objB[0],objB[1])
    CV.print_objects(objC[0],objC[1])


    return [objA,objB,objC]


def find_one_object(sample_sig, current_sig, current_x, current_y,current_theta, first_degree, filename):

    objA=[]
   # objB=[]
   # objC=[]
    subtract_list=[]

    for i in range(len(sample_sig)):
        if sample_sig[i]>200:
            subtract_list.append(0)
        else:
            subtract_list.append(sample_sig[i]-current_sig[i])

    for i in range(len(subtract_list)):
        if subtract_list[i] < 15:
            subtract_list[i]=0
  #  plt.scatter(range(len(subtract_list)),subtract_list)
    #print("size of subtract list:", len(subtract_list))
    
   # plt.savefig(fname = filename)

    polA=find_object_polar(subtract_list, current_sig, first_degree)
   # polB=find_object_polar(90,270,subtract_list, current_sig)
   # polC=find_object_polar(270,360,subtract_list, current_sig)

    #print(polA)
   # print(polB)
   # print(polC)

    objA = polar_to_cartesian(current_x, current_y, polA[0],polA[1]+current_theta)
    #print(objA)
  #  objB = polar_to_cartesian(current_x, current_y, polB[0],polB[1])
  #  objC = polar_to_cartesian(current_x, current_y, polC[0],polC[1])

    #update web GUI with cylinders
    wall_corners=[[0,0],[0,168],[84,168],[84,126],[84,210],[168,210],[168,84],[210,84],[210,0]]
    CV = canvas(wall_corners)
    CV.print_objects(objA[0],objA[1])
   # CV.print_objects(objB[0],objB[1])
   # CV.print_objects(objC[0],objC[1])




    return objA

def polar_to_cartesian(x_initial, y_initial, distance, theta):
    x_final = x_initial+distance*math.cos(math.radians(theta))
    y_final = y_initial+distance*math.sin(math.radians(theta))

    return [x_final,y_final]


#returns object in form [distance,theta]
def find_object_polar(subtract_list,current_sig, first_degree):
    obj=[]
    longest_list=[]
    longest_counter=0
    #TODO:- this for loop might have problem
    for i in range(len(subtract_list)):
        if subtract_list[i] > 0:
            longest_counter+=1
            
        else:
            longest_counter=0
        longest_list.append(longest_counter)
    longest_list = np.array(longest_list)
    theta = (longest_list.argmax() - round(longest_list.max()/2)) * bin_size+first_degree
    print("theta relative to robot:", theta)
    distance = current_sig[int(longest_list.argmax() - round(longest_list.max()/2))]
  #  print("theta:", theta)
  #  print("distance:", distance)
    obj.append(distance)
    obj.append(theta)
    return obj


def mean_of_signatures(sig_1, sig_2, sig_3):
    final_sig = []
    for i in range(len(sig_1)):
        final_sig.append((sig_1[i] + sig_2[i] + sig_3[i]) / 3)
    
    return final_sig



def find_min_x(sig):
    
    x_list = np.array(sig)
    print(x_list)
    
    minX = x_list.min()
    mins_bool_array = (x_list==minX)
    indeces = np.arange(0,len(x_list))
    indexed_list = indeces[mins_bool_array]
    arg_min = round(indexed_list.mean())
    
    #thetha =. diff_from_90*bin_size
    angle_offset = -( arg_min-round(len(x_list)/2) )*bin_size
    
    return [minX, angle_offset]


signatures = SignatureContainer(5);
#signatures.delete_loc_files()

#learn_location();
#recognize_location();
