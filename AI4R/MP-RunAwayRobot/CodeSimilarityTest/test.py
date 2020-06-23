import pycode_similar

str1 = """def estimate_next_pos(measurement, OTHER = None):
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
        # You must return xy_estimate (x, y), and OTHER (even if it is None) 
        # in this order for grading purposes.
        return xy_estimate, OTHER"""

str2 = """def estimate_next_pos(measurement, OTHER=None):
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
        # You must return xy_estimate (x, y), and OTHER (even if it is None)
        # in this order for grading purposes.
        OTHER.append(measurement)
        return xy_estimate, OTHER"""

print(pycode_similar.detect([str1,str2]))
