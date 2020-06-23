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
    N = 10
    it = 0
    sig_noise = measurement_noise
    if(OTHER!=None):
        print("It IF")
        it = OTHER[3]
        
    
    if(OTHER == None):
        print("First IF") 
        xy_estimate = [measurement[0],measurement[1]]
        it += 1
        OTHER = [measurement,alpha1,None,it]
        

    elif(OTHER[1] == None):
        print("Second IF")
        old_x,old_y = OTHER[0]
        x,y = measurement
        distance = distance_between(measurement,OTHER[0])
        alpha1 = atan2((y-old_y),(x-old_x))
        xy_estimate = [measurement[0],measurement[1]]
        it += 1
        OTHER = [measurement,alpha1,None,it]
        
        
    elif( it < 3 ):
        print("Third IF")
        alpha1 = OTHER[1]
        old_x,old_y = OTHER[0]
        x,y = measurement
        distance = distance_between(measurement,OTHER[0])
        alpha2 = atan2((y-old_y),(x-old_x))
        turn = (alpha2-alpha1)
        p = []
        for i in range(N):
            r = robot(random.gauss(measurement[0],sig_noise),random.gauss(measurement[1],sig_noise),
                      random.gauss(alpha2,sig_noise),
                      random.gauss(turn,sig_noise),
                      random.gauss(distance,sig_noise))
            p.append(r)
        print("Created P")
        for i in range(N):
            print(p[i].sense())

        p2 = []
        print("Moving P")
        for i in range(N):
            p[i].move(random.gauss(p[i].turning,0.001),random.gauss(p[i].distance,0.001))#move_in_circle()
            print(p[i].sense())
            p2.append(p[i])
        p = p2

        print("Moved P")
        for i in range(N):
            print(p[i].sense())
        x = 0
        y = 0
        for i in range(N):
            x += p[i].x
            y += p[i].y
        x = x/N
        y = y/N
        xy_estimate = [x,y]
        it += 1
        print("BeforeOther")
        for i in range(N):
            print(p[i].sense())
        OTHER = [measurement,alpha1,p,it]
        
        #print(xy_estimate)
    else:
        print("last else")
        p = OTHER[2]
        print("Retrieved p")
        for i in range(N):
            print(p[i].sense())
        alpha1 = OTHER[1]
        prev_pred = measurement
        w = []
        print("Probabilities")
        for i in range(N):
            current_measurement= p[i].sense()
            error = distance_between(current_measurement,prev_pred)
            prob = exp(1/(error))
            w.append(prob)
            print(w[i])

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

        print("Sampled P")
        for i in range(N):
            print(p[i].sense())

        p2 = []
        print("Moving P")
        for i in range(N):
            p[i].move(random.gauss(p[i].turning,0.001),random.gauss(p[i].distance,0.001))#move_in_circle()
            print(p[i].sense())
            p2.append(p[i])
        p = p2

        print("Moved P")
        for i in range(N):
            print(p[i].sense())
        
        x = 0.0
        y = 0.0
        for i in range(len(p)):
            x += p[i].x
            y += p[i].y
        x = x/len(p)
        y = y/len(p)
        xy_estimate = [x,y]
        it += 1
        print("BeforeOther")
        for i in range(N):
            print(p[i].sense())
        OTHER = [measurement,alpha1,p,it]
        
        
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
measurement_noise = 0.1 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)

demo_grading(estimate_next_pos, test_target)
#position_guess,OTHER = estimate_next_pos(test_target.sense(), OTHER=None)
#print(test_target.sense())
#print(position_guess)
#test_target.move_in_circle()
#print(test_target.sense())
