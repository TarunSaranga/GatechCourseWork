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

    
    return turning, distance, OTHER
