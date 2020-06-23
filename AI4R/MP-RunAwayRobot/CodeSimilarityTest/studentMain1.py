from robot import *
from math import *
from matrix import *
import random


def estimate_next_pos(measurement, OTHER = None):
    
    if OTHER == None:
        OTHER = []
        old_x = measurement[0]
        old_y = measurement[1]
    else:
        old_x = OTHER[-1][0]
        old_y = OTHER[-1][1]

    x = measurement[0]
    y = measurement[1]

    if len(OTHER) >= 3:
        old2_x = OTHER[-2][0]
        old2_y = OTHER[-2][1]
    else:
        old2_x = old_x
        old2_y = old_y
    alpha1 = atan2((y - old_y), (x - old_x))
    alpha2 = atan2((old_y - old2_y), (old_x - old2_x))
    turn = alpha1 - alpha2
    d = distance_between([x,y],[old_x,old_y])

    x_new = x + d * cos(turn + alpha1)
    y_new = y + d * sin(turn + alpha1)
    xy_estimate = [x_new, y_new]
    OTHER.append(measurement)
    
    return xy_estimate, OTHER

