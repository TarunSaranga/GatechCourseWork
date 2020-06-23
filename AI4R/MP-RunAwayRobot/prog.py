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
    if(OTHER==None):
        p = []
        N = 1000
        #print("First time")
        for i in range(N):
            r = robot(measurement[0],measurement[1], random.random(), random.random()*pi ,random.random()*3)
            p.append(r)
            #print(p[i].sense())
            
        #print("Moving in Circle")
        p77 = []
        for i in range(N):
            p[i].move(random.gauss(p[i].turning,0.01),random.gauss(p[i].distance,0.01))
            #print(p[i].sense())
            p77.append(p[i])
        p = p77
                
        x = 0.0
        y = 0.0
        for i in range(len(p)):
            x += p[i].x
            y += p[i].y
        x = x/len(p)
        y = y/len(p)
        xy_estimate = [x,y]
        #print("xy_estimate")
        #print(xy_estimate)
        #print()
        OTHER = p   
    else:
        #print("Next time")
        p = OTHER
        #print("Retrieved p")
        #for i in range(len(p)):
           #print(p[i].sense())
        
        prev_position = measurement
        #print("true Position")
        #print(prev_position)
        #print()
        #print("Probabilities")
        w = []
        measurment_prob = []
        for i in range(len(p)):
            current_measurement = p[i].sense()
            #current_measurement = distance_between(current_measurement,[0,0])
            error = distance_between(current_measurement,measurement)#distance_between([0,0], measurement)
            prob = 1/(3**error)#exp(- ((error - current_measurement) ** 2) / ((0.05*1.5) ** 2) / 2.0) / sqrt(2.0 * pi * ((0.05*1.5) ** 2))
            w.append(prob)
            #print(w[i])
        p3 = []
        index = int(random.random() * len(p))
        beta = 0.0
        mw = max(w)
        #print(mw)
        for i in range(len(p)):
            beta += random.random() * 2.0 * mw
            while beta > w[index]:
                       beta -= w[index]
                       index = (index + 1) % len(p)
            p3.append(p[index])
        p = p3
        #print()
        #print("Sampled P")
        #for i in range(len(p)):
        #    print(p[i].sense())
        
        #print()
        #print("Moving selected Paricles")
        p2 = []
        for i in range(len(p)):
            p[i].move(random.gauss(p[i].turning,0.1),random.gauss(p[i].distance,0.1))
            #print(p[i].sense())
            p2.append(p[i])    
        p = p2
        
        #print()
        x = 0.0
        y = 0.0
        for i in range(len(p)):
            x += p[i].x
            y += p[i].y
        x = x/len(p)
        y = y/len(p)
        xy_estimate = [x,y]
        #print("xy_estimate")
        #print(xy_estimate)
        #print("before Other")
        #for i in range(len(p)):
        #    print(p[i].sense())
        #if(mw <0.9):
        #    p = []
        #    for i in range(10):
        #        r = robot(measurement[0],measurement[1], random.random()*2*pi-pi, random.random()*2*pi-pi ,random.random()*2)
        #        p.append(r)
        #        #p[i].move_in_circle()
        #    OTHER = p
        #else:
        OTHER = p
        #print("OTHER[0]")
        #print(OTHER[0])
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
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        #print(measurement)
        #print(position_guess)
        #print(true_position)
        #print()
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
