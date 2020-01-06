from random import *
import math


wall_corners=[[0,0],[0,168],[84,168],[84,126],[84,210],[168,210],[168,84],[210,84],[210,0]]

def calc_m(vertex_A, vertex_B, x, y, theta): #assuming  theta is given as degrees
    numerator = (vertex_B[1]-vertex_A[1])*(vertex_A[0]-x)-(vertex_B[0]-vertex_A[0])*(vertex_A[1]-y)
    denom = (vertex_B[1]-vertex_A[1])*math.cos(math.radians(theta))-(vertex_B[0]-vertex_A[0])*math.sin(math.radians(theta))
    if denom ==0:
        return -1    
    return (numerator/denom)

def is_within_bounds(vertex_A, vertex_B, point_C):
    max_x = max(vertex_A[0],vertex_B[0])
    min_x = min(vertex_A[0],vertex_B[0])
    max_y = max(vertex_A[1],vertex_B[1])
    min_y = min(vertex_A[1],vertex_B[1])
    if point_C[0] <= max_x and point_C[0] >= min_x and point_C[1] <= max_y and point_C[1] >= min_y: 
        return True
    else:
        return False
    
    
    
def pick_m(m_list, wall_corners, x, y, theta):
    for i in range(len(m_list)):
        if m_list[i] > 0:
            new_x = x + m_list[i] * math.cos(math.radians(theta))
            new_y = y + m_list[i] * math.sin(math.radians(theta))
            if i != len(m_list) - 1: # this check is to ensure array wraps around from last element to first
                if is_within_bounds(wall_corners[i],wall_corners[i+1],[new_x, new_y]):
                    return m_list[i]
            else:
                if is_within_bounds(wall_corners[i],wall_corners[0],[new_x, new_y]):
                    return m_list[i]
    return "No eligible m"

def test_calc_pdf(BP):
    #calculate_pdf(self, actual_val, mean, st_dev, offset):
    z_m = [-20, -10, -5, 0, 5, 10, 20, 50, 100]
    for i in range(len(z_m)):
        print(z_m, ": ", BP.calculate_pdf(av, 0, 3, 0.005))

def calc_likelihood(x, y, theta, z):
    m_list = []
    for i in range(len(wall_corners)):
        if i!=len(wall_corners)-1:
            m_list.append(calc_m(wall_corners[i],wall_corners[i+1],x,y,theta))
        else:
            m_list.append(calc_m(wall_corners[i],wall_corners[0],x,y,theta))
    m = pick_m(m_list, wall_corners, x, y, theta)
    likelihood = norm.pdf(z-m, loc= 0, scale=0.5) +0.1 # +0.1 to make the prediction robust against sonar anomalies
    return likelihood
        
    