# ----------
# Part Four
#
# Again, you'll track down and recover the runaway Traxbot. 
# But this time, your speed will be about the same as the runaway bot. 
# This may require more careful planning than you used last time.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time. 
#
# ----------
# GRADING
# 
# Same as part 3. Again, try to catch the target in as few steps as possible.

from robot import *
from math import *
from matrix import *
import random

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    # This function will be called after each time the target moves. 
    sigma = 0.05
    
    F = matrix([[1., 1., 0.],
                [0., 1., 0.],
                [0., 0., 1.]])      # next state function
    H = matrix([[1., 0., 0.],
                [0., 0., 1.]])      # measurement function
    R = matrix([[sigma, 0.],
                [0., sigma]])          # measurement uncertainty
    I = matrix([[1., 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]])      # identity matrix

    class KalmanFilter:                #Inspired from Kalman Filter implementations available on the web
    # u = matrix([[0.], [0.], [0.]])  # external motion
        def __init__(self, sigma):
            self.x = matrix([[0.],
                             [0.],
                             [0.]])
            self.P = matrix([[1000., 0., 0.],
                             [0., 1000., 0.],
                             [0., 0., 1000.]])
            # measurement uncertainty
            self.R = matrix([[sigma, 0.],
                            [0., sigma]])
            # next state function
            self.F = matrix([[1., 1., 0.],
                             [0., 1., 0.],
                             [0., 0., 1.]])
            # measurement function
            self.H = matrix([[1., 0., 0.],
                             [0., 0., 1.]])
            # identity matrix
            self.I = matrix([[1., 0., 0.],
                             [0., 1., 0.],
                             [0., 0., 1.]])
            self.keep = []

        def predict(self, measurement):
            self.keep.append(measurement)
            # calculate heading and distance from previous data
            if len(self.keep) == 1:
                measured_heading = 0
                measured_distance = 0
            else:
                p1 = (self.keep[-1][0], self.keep[-1][1])
                p2 = (self.keep[-2][0], self.keep[-2][1])
                measured_distance = distance_between(p1, p2)
                dx = p1[0] - p2[0]
                dy = p1[1] - p2[1]
                measured_heading = atan2(dy, dx) % (2 * pi)
                self.keep.pop(0)
    
            prev_heading = self.x.value[0][0]
            for d in [-1, 0, 1]:
                diff = (int(prev_heading / (2 * pi)) + d) * (2 * pi)
                if abs(measured_heading + diff - prev_heading) < pi:
                    measured_heading += diff
                    break
            # measurement update
            y = matrix([[measured_heading],
                        [measured_distance]]) - self.H * self.x
            S = self.H * self.P * self.H.transpose() + self.R
            K = self.P * self.H.transpose() * S.inverse()
            self.x = self.x + (K * y)
            self.P = (self.I - K * self.H) * self.P
            # prediction
            self.x = self.F * self.x
            self.P = self.F * self.P * self.F.transpose()
    
            estimated_heading = self.x.value[0][0]
            estimated_distance = self.x.value[2][0]
            estimated_next = next_position_in_circle(measurement[0], measurement[1],
                                               estimated_heading, estimated_distance)
            return estimated_next
    
    def next_position_in_circle(x, y, heading, distance):
        estimated_x = x + distance * cos(heading)
        estimated_y = y + distance * sin(heading)
        return estimated_x, estimated_y

    def next_pos(measurement, OTHER=None):
        if not OTHER:
            OTHER = [KalmanFilter(0.05),]
        predictor = OTHER[0]
        estimated_next = predictor.predict(measurement)

        return estimated_next, OTHER

    estimated_target_pos, OTHER = next_pos(target_measurement, OTHER)
    estimated_distance = distance_between(hunter_position, estimated_target_pos)
    steps = 1
    x = OTHER[0].x
    while estimated_distance > steps * max_distance:
        x = F * x
        estimated_target_pos = next_position_in_circle(estimated_target_pos[0], estimated_target_pos[1],
                                                 x.value[0][0], x.value[2][0])
        estimated_distance = distance_between(hunter_position, estimated_target_pos)
        steps += 1

    heading_to_target = get_heading(hunter_position, estimated_target_pos)

    turning = heading_to_target - hunter_heading
    turning = angle_trunc(turning)

    if estimated_distance > max_distance:
        distance = max_distance  # full speed ahead!
    else:
        distance = estimated_distance
    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.
    return turning, distance, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 0.98 * target_bot.distance # 0.98 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)
        
        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1            
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught



def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER

#target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
#measurement_noise = .05*target.distance
#target.set_noise(0.0, 0.0, measurement_noise)

#hunter = robot(-10.0, -10.0, 0.0)

#print demo_grading(hunter, target, next_move)





