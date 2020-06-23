from math import *
import random


def angle_trunc(a):
    """Helper function to map all angles onto [-pi, pi]

    Arguments:
        a(float): angle to truncate.

    Returns:
        angle between -pi and pi.
    """
    return ((a + pi) % (pi * 2)) - pi


class robot:
    """Robot simulator.

    Attributes:
        random_move_count(int): number of moves before randomly disobeying a move command
        move_counter(int): current move count.
        x(float): x position.
        y(float): y position.
        heading(float): angle currently facing with 0 being east.
        turning(float): angle to turn each time a turn is taken.
        distance(float): distance to travel for each move.
        line_length(int): number of times to travel straight before executing a turn.
        line_count(int): how many straight segments the robot has traveled so far since last turn.
        turning_noise(float): turning noise.
        distance_noise(float): distance traveled noise.
        measurement_noise(float): noise of location measurement.
    """

    def __init__(self, x=0.0, y=0.0, heading=0.0, turning=2 * pi / 10, distance=1.0, line_length=1, random_move=None):
        """This function is called when you create a new robot. It sets some of
        the attributes of the robot, either to their default values or to the values
        specified when it is created.

        Set random_move = None to turn off random movements.
        """
        self.random_move_count = random_move
        self.move_counter = 0
        self.x = x
        self.y = y
        self.heading = heading
        self.turning = turning  # only applies to target robots who constantly move in a circle
        self.distance = distance  # only applies to target bot, who always moves at same speed.
        self.line_length = line_length  # If not one, robot moves in straight lines for line_length steps.
        self.line_count = 0  # How many straight segments have we done with no turn so far?
        self.turning_noise = 0.0
        self.distance_noise = 0.0
        self.measurement_noise = 0.0

    def set_noise(self, new_t_noise, new_d_noise, new_m_noise):
        """This lets us change the noise parameters, which can be very
        helpful when using particle filters.

        Arguments:
            new_t_noise(float): turning noise to set.
            new_d_noise(float): distance noise to set.
            new_m_noise(float): measurement noise to set.
        """
        self.turning_noise = float(new_t_noise)
        self.distance_noise = float(new_d_noise)
        self.measurement_noise = float(new_m_noise)

    def move(self, turning, distance, tolerance=0.001, max_turning_angle=pi):
        """This function turns the robot and then moves it forward.

        Arguments:
            turning(float): angle to turn.
            distance(float): distance to travel.
            tolerance(float): deprecated.
            max_turning_angle(float): max allowed turn.
                defaults to pi.
        """
        if self.random_move_count and self.move_counter and self.move_counter % self.random_move_count is 0:
            rand_change = random.uniform(0, 1)
            # randomly adjust turning
            turning = turning * rand_change
            # randomly adjust distance
            distance = distance * rand_change

        self.move_counter += 1

        # apply noise, this doesn't change anything if turning_noise
        # and distance_noise are zero.
        turning = random.gauss(turning, self.turning_noise)
        distance = random.gauss(distance, self.distance_noise)

        # truncate to fit physical limitations
        turning = max(-max_turning_angle, turning)
        turning = min(max_turning_angle, turning)
        distance = max(0.0, distance)

        # Execute motion
        self.heading += turning
        self.heading = angle_trunc(self.heading)
        self.x += distance * cos(self.heading)
        self.y += distance * sin(self.heading)

    def move_in_circle(self):
        """This function is used to advance the runaway target bot.
        """
        self.move(self.turning, self.distance)

    def move_in_polygon(self):
        """This function is used to advance the runaway target bot in a polygon shape.
        """

        if self.line_count == self.line_length:
            self.move_in_circle()
            self.line_count = 0
        else:
            self.move(0.0, self.distance)

        self.line_count = self.line_count + 1

    def sense(self):
        """This function represents the robot sensing its location. When
        measurements are noisy, this will return a value that is close to,
        but not necessarily equal to, the robot's (x, y) position.

        Returns:
            Sensor location measurement based on measurement noise.
        """
        return (random.gauss(self.x, self.measurement_noise),
                random.gauss(self.y, self.measurement_noise))

    def __repr__(self):
        """This allows us to print a robot's position

        Returns:
            String representation of robot that is the x and y location.
        """
        return '[%.5f, %.5f]' % (self.x, self.y)
