from robot import *
from math import *
from matrix import *
import random

    # This function will be called after each time the target moves. 
    # The OTHER variable is a place for you to store any historical 
    # information about the progress of the hunt (or maybe some 
    # localization information). Your must return a tuple of three 
    # values: turning, distance, OTHER

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):

    def get_heading(hunter_position, target_position):
        """Returns the angle, in radians, between the target and hunter positions"""
        hunter_x, hunter_y = hunter_position
        target_x, target_y = target_position
        heading = atan2(target_y - hunter_y, target_x - hunter_x)
        heading = angle_trunc(heading)
        return heading
    
    def distance_between(point1, point2):
        """Computes distance between point1 and point2. Points are (x, y) pairs."""
        x1, y1 = point1
        x2, y2 = point2
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def estimate_next_pos(measurement, OTHER = None):
        """Estimate the next (x, y) position of the wandering Traxbot
        based on noisy (x, y) measurements."""
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
    
        return xy_estimate, OTHER
    # Using the template from naive_nest_pos 
    target_prediction = target_measurement
    if not OTHER:  # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings)  # now I can keep track of history
    else:  # not the first time, update my history
        target_prediction, null = estimate_next_pos(target_prediction, OTHER[0])
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER  # now I can always refer to these variables

    heading_to_target = get_heading(hunter_position, target_prediction)
    heading_difference = angle_trunc(heading_to_target - hunter_heading)
    turning = heading_difference  # turn towards the target
    distance = min(max_distance, distance_between(hunter_position, target_prediction))  # full speed ahead!
    
    return turning, distance, OTHER

