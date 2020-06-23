# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *
from math import *
from matrix import *
import random


    # This is the function you have to write. The argument 'measurement' is a 
    # single (x, y) point. This function will have to be called multiple
    # times before you have enough information to accurately predict the
    # next position. The OTHER variable that your function returns will be 
    # passed back to your function the next time it is called. You can use
    # this to keep track of important information over time.

def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    #A Geometric Solution to the problem
    def distance_between(point1, point2):
        """Computes distance between point1 and point2. Points are (x, y) pairs."""
        x1, y1 = point1
        x2, y2 = point2
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    if OTHER == None:
        OTHER = []
        old_x, old_y = measurement
    else:
        old_x, old_y = OTHER[-1]

    x,y = measurement

    if len(OTHER) >= 3:
        old2_x, old2_y = OTHER[-2]
    else:
        old2_x, old2_y = old_x, old_y
        
    alpha1 = atan2((y - old_y), (x - old_x))
    alpha2 = atan2((old_y - old2_y), (old_x - old2_x))
    turn = alpha1 - alpha2
    d = distance_between([x,y],[old_x,old_y])
    #From the equations derived in the class
    x_new = x + d * cos(turn + alpha1) 
    y_new = y + d * sin(turn + alpha1)
    xy_estimate = [x_new, y_new]
    OTHER.append(measurement)
    
    return xy_estimate, OTHER
