

from matrix import *

from robot import *



def estimate_next_pos(measurement, OTHER=None):
    
    if OTHER is None:
        OTHER = []
        x_old = measurement[0]
        y_old = measurement[1]
    else:
        x_old = OTHER[-1][0]
        y_old = OTHER[-1][1]

    x = measurement[0]
    y = measurement[1]

    if len(OTHER) >= 3:
        x_old2 = OTHER[-2][0]
        y_old2 = OTHER[-2][1]
    else:
        x_old2 = x_old
        y_old2 = y_old
    bearing = atan2(y - y_old, x - x_old)
    bearing_old = atan2(y_old - y_old2, x_old - x_old2)
    theta = bearing - bearing_old
    d = sqrt((y - y_old) ** 2 + (x - x_old) ** 2)

    x_new = x + d * cos(theta + bearing)
    y_new = y + d * sin(theta + bearing)
    xy_estimate = (x_new, y_new)
    
    OTHER.append(measurement)
    return xy_estimate, OTHER


