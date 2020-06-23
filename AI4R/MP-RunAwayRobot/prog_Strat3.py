from robot import *
from math import *
#from matrix import *
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
    alpha1 = None
    N = 1000
    it = 0
    sig_noise = 0.05*1.5
    if(OTHER!=None):
        it = OTHER[3]

    #sig_noise = 0.01
    #h_noise = 0.01
    #t_noise = 0.001
    #sss = 0
    #for i in range(10000):
    #    sss += random.gauss(measurement[0],noise)
    measured_x = measurement[0]#sss/10000
    #sss = 0
    #for i in range(10000):
    #    sss += random.gauss(measurement[1],noise)
    measured_y = measurement[1]#sss/10000
    print("Recovered measurement",[measured_x,measured_y])
    if(OTHER == None):
        p=[]
        x = 0
        y = 0
        xy_estimate = [x,y]
        it += 1
        OTHER = [[measured_x,measured_y],alpha1,p,it]
        #print(xy_estimate)
    elif(OTHER[1] == None):
        #print("in else")
        p = []
        old_x,old_y = OTHER[0]
        x,y = measured_x,measured_y
        distance = distance_between([measured_x,measured_y],OTHER[0])
        alpha1 = atan2((y-old_y),(x-old_x))
        p1 = []
        x = 0
        y = 0
        xy_estimate = [x,y]
        it += 1
        OTHER = [[measured_x,measured_y],alpha1,p,it]
        #print(xy_estimate)
    elif(it<=3):
        alpha1 = OTHER[1]
        old_x,old_y = OTHER[0]
        x,y = measured_x,measured_y
        distance = distance_between([measured_x,measured_y],OTHER[0])
        alpha2 = atan2((y-old_y),(x-old_x))
        turn = (alpha2-alpha1)
        p2 = []
        for i in range(N):
            r = robot(random.gauss(measured_x,sig_noise),random.gauss(measured_y,sig_noise), random.gauss(alpha2,sig_noise), random.gauss(turn,sig_noise), random.gauss(distance,sig_noise))
            p2.append(r)
            p2[i].move(random.gauss(p2[i].turning,0.1),random.gauss(p2[i].distance,0.1))#move_in_circle()
            x += p2[i].x
            y += p2[i].y
        p = p2
        x = x/N
        y = y/N
        xy_estimate = [x,y]
        it += 1
        OTHER = [[measured_x,measured_y],alpha1,p,it]
        #print(xy_estimate)
    else:
        p = OTHER[2]
        prev_pred = measurement
        w = []
        for i in range(N):
            current_measurement= p[i].sense()
            error = distance_between(current_measurement,prev_pred)
            prob = 1/(error)
            w.append(prob)

        p3 = []
        index = int(random.random() * N)
        beta = 0.0
        mw = max(w)
        #print(mw)
        for i in range(N):
            beta += random.random() * 2.0 * mw
            while beta > w[index]:
                       beta -= w[index]
                       index = (index + 1) % len(p)
            p3.append(p[index])
        p = p3

        p2 = []
        for i in range(N):
            p[i].move(random.gauss(p[i].turning,sig_noise),random.gauss(p[i].distance,sig_noise))
            #print(p[i].sense())
            p2.append(p[i])    
        p = p2

        x = 0.0
        y = 0.0
        for i in range(len(p)):
            x += p[i].x
            y += p[i].y
        x = x/len(p)
        y = y/len(p)
        xy_estimate = [x,y]
        it += 1
        OTHER = [[measured_x,measured_y],alpha1,p,it]
        
    print("ITER",it)   
    
    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    return xy_estimate, OTHER 

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    #For Visualization
    import turtle    #You need to run this locally to use the turtle module
    window = turtle.Screen()
    window.bgcolor('white')
    size_multiplier= 25.0  #change Size of animation
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.1, 0.1, 0.1)
    measured_broken_robot = turtle.Turtle()
    measured_broken_robot.shape('circle')
    measured_broken_robot.color('red')
    measured_broken_robot.resizemode('user')
    measured_broken_robot.shapesize(0.1, 0.1, 0.1)
    prediction = turtle.Turtle()
    prediction.shape('arrow')
    prediction.color('blue')
    prediction.resizemode('user')
    prediction.shapesize(0.1, 0.1, 0.1)
    prediction.penup()
    broken_robot.penup()
    measured_broken_robot.penup()
    #End of Visualization
    while not localized and ctr <= 1000:
        ctr += 1
        measurement = target_bot.sense()
        print("measurement: ",measurement)
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        print("position_guess: ",position_guess)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        print("True Position: ",true_position)
        error = distance_between(position_guess, true_position)        
        print("error",error)
        print()
        if error <= distance_tolerance:
            print( "You got it right! It took you ", ctr, " steps to localize.")
            localized = True
        if ctr == 1000:
            print( "Sorry, it took you too many steps to localize the target.")
        #More Visualization
        measured_broken_robot.setheading(target_bot.heading*180/pi)
        measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
        measured_broken_robot.stamp()
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
        broken_robot.stamp()
        prediction.setheading(target_bot.heading*180/pi)
        prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
        prediction.stamp()
        #End of Visualization
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 0.05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)

demo_grading(estimate_next_pos, test_target)
#position_guess,OTHER = estimate_next_pos(test_target.sense(), OTHER=None)
#print(test_target.sense())
#print(position_guess)
#test_target.move_in_circle()
#print(test_target.sense())
