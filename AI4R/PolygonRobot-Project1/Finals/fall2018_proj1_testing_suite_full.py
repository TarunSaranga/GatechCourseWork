#!/usr/bin/python

import math
import random
import robot
import unittest
import multiprocessing as mproc
import traceback

try:
    import studentMain1
except Exception as e:
    print "Error importing studentMain1:", e

try:
    import studentMain2
except Exception as e:
    print "Error importing studentMain2:", e

try:
    import studentMain3
except Exception as e:
    print "Error importing studentMain3:", e

try:
    import studentMain4
except Exception as e:
    print "Error importing studentMain4:", e


PI = math.pi

GLOBAL_SEEDS = [None,
                None,
                'air_nomads',
                'water_tribes',
                'earth_kingdom',
                'fire_nation']

TIME_LIMIT = 5  # seconds

CREDIT_PER_PASS = 2.5  # points

GLOBAL_PARAMETERS = [None,
 {'test_case': 1,
     'target_x': -5.86370643627,
     'target_y': -18.3979624504,
     'target_heading': -2.54085637477,
     'target_period': 12,
     'target_speed': 1.77584114242,
     'target_line_length': 8, 
     'hunter_x': 4.84183985557,
     'hunter_y': 5.62143822235,
     'hunter_heading': -2.08377781921,
     'random_move': 20
    },
    {'test_case': 2,
     'target_x': -7.30880841813,
     'target_y': -7.5606752408,
     'target_heading': 2.69362855848,
     'target_period': 3,
     'target_speed': 1.51140830722,
     'target_line_length': 2, 
     'hunter_x': -5.72203926243,
     'hunter_y': 0.516750503883,
     'hunter_heading': 2.93680309891,
     'random_move': 20
    },
    {'test_case': 3,
     'target_x': -16.9919036943,
     'target_y': -5.37915688968,
     'target_heading': 2.8502816235,
     'target_period': 12,
     'target_speed': 3.96162073429,
     'target_line_length': 5, 
     'hunter_x': 15.2086062211,
     'hunter_y': 6.58071166693,
     'hunter_heading': 1.76911053982,
     'random_move': 20
    },
    {'test_case': 4,
     'target_x': -12.8136631315,
     'target_y': -12.3915725485,
     'target_heading': 2.29530869623,
     'target_period': 4,
     'target_speed': 3.52236333443,
     'target_line_length': 12, 
     'hunter_x': 0.101988617677,
     'hunter_y': 18.6497565572,
     'hunter_heading': -2.88423229835,
     'random_move': 20
    },
    {'test_case': 5,
     'target_x': -9.95917579167,
     'target_y': -19.0224686649,
     'target_heading': -0.595304624294,
     'target_period': 10,
     'target_speed': 4.30253727555,
     'target_line_length': 1, 
     'hunter_x': 6.71240390289,
     'hunter_y': 17.156900913,
     'hunter_heading': 2.05982553331,
     'random_move': 20
    },
    {'test_case': 6,
     'target_x': -18.2140984291,
     'target_y': 9.42549782318,
     'target_heading': -2.57058246946,
     'target_period': -11,
     'target_speed': 2.08032206719,
     'target_line_length': 1, 
     'hunter_x': -17.2193581055,
     'hunter_y': -11.7666921612,
     'hunter_heading': -0.273102394155,
     'random_move': 20
    },
    {'test_case': 7,
     'target_x': -3.25961072211,
     'target_y': -3.45921736193,
     'target_heading': 1.12396926556,
     'target_period': 9,
     'target_speed': 3.29449778851,
     'target_line_length': 14, 
     'hunter_x': -18.7022301072,
     'hunter_y': 12.6171283902,
     'hunter_heading': 0.340266564211,
     'random_move': 20
    },
    {'test_case': 8,
     'target_x': -5.64991834879,
     'target_y': -1.44292880086,
     'target_heading': -1.97090548672,
     'target_period': -5,
     'target_speed': 3.44453451627,
     'target_line_length': 4, 
     'hunter_x': -7.98483716048,
     'hunter_y': 6.14380675819,
     'hunter_heading': -1.56183988278,
     'random_move': 20
    },
    {'test_case': 9,
     'target_x': -16.928030136,
     'target_y': 0.215918834076,
     'target_heading': -2.16135467699,
     'target_period': 11,
     'target_speed': 1.05265361981,
     'target_line_length': 2, 
     'hunter_x': 9.3688902426,
     'hunter_y': 10.5895961612,
     'hunter_heading': -3.08144211568,
     'random_move': 20
    },
    {'test_case': 10,
     'target_x': -0.826697380063,
     'target_y': 11.8532999942,
     'target_heading': 0.130432643617,
     'target_period': 4,
     'target_speed': 3.73713821483,
     'target_line_length': 7, 
     'hunter_x': 12.5185039397,
     'hunter_y': 10.1212436328,
     'hunter_heading': 0.702958578243,
     'random_move': 20
    }                    

]


class RunawaySimulator:
    """Run student submission code.

    Attributes:
        robot_steps(Queue): synchronized queue to store robot steps.
        robot_found(Queue): synchronized queue to store if robot found.
        robot_error(Queue): synchronized queue to store exception messages.
    """
    def __init__(self):
        self.robot_steps = mproc.Queue(1)
        self.robot_found = mproc.Queue(1)
        self.robot_error = mproc.Queue(1)

    def _reset(self):
        """Reset submission results.
        """
        while not self.robot_steps.empty():
            self.robot_steps.get()

        while not self.robot_found.empty():
            self.robot_found.get()

        while not self.robot_error.empty():
            self.robot_found.get()

    @staticmethod
    def distance(p, q):
        """Calculate the distance between two points.

        Args:
            p(tuple): point 1.
            q(tuple): point 2.

        Returns:
            distance between points.
        """
        x1, y1 = p
        x2, y2 = q

        dx = x2 - x1
        dy = y2 - y1

        return math.sqrt(dx**2 + dy**2)

    @staticmethod
    def truncate_angle(t):
        """Truncate angle between pi and -pi.

        Args:
            t(float): angle to truncate.

        Returns:
            truncated angle.
        """
        return ((t + PI) % (2 * PI)) - PI

    def simulate_without_hunter(self, estimate_next_pos, params):
        """Run simulation only to locate lost bot.

        Args:
            estimate_next_pos(func): Student submission function to estimate next robot position.
            params(dict): Test parameters.

        Raises:
            Exception if error running submission.
        """
        self._reset()

        target = robot.robot(params['target_x'],
                             params['target_y'],
                             params['target_heading'],
                             2.0 * PI / params['target_period'],
                             params['target_speed'],
                             params['target_line_length'],
                             params['random_move'])
        target.set_noise(0.0,
                         0.0,
                         params['noise_ratio'] * params['target_speed'])

        tolerance = params['tolerance_ratio'] * target.distance
        other_info = None
        steps = 0

        random.seed(GLOBAL_SEEDS[params['part']])

        try:
            while steps < params['max_steps']:
                target_meas = target.sense()

                estimate, other_info = estimate_next_pos(target_meas, other_info)

                target.move_in_polygon()
                target_pos = (target.x, target.y)

                separation = self.distance(estimate, target_pos)
                if separation < tolerance:
                    self.robot_found.put(True)
                    self.robot_steps.put(steps)
                    return

                steps += 1

            self.robot_found.put(False)
            self.robot_steps.put(steps)

        except:
            self.robot_error.put(traceback.format_exc())

    def simulate_with_hunter(self, next_move, params):
        """Run simulation to locate lost bot and catch with hunter.

        Args:
            next_move(func): Student submission function for hunters next move.
            params(dict): Test parameters.

        Raises:
            Exception if error running submission.
        """
        self._reset()

        target = robot.robot(params['target_x'],
                             params['target_y'],
                             params['target_heading'],
                             2.0 * PI / params['target_period'],
                             params['target_speed'],
                             params['target_line_length'],
                             params['random_move'])
        target.set_noise(0.0,
                         0.0,
                         params['noise_ratio'] * params['target_speed'])

        hunter = robot.robot(params['hunter_x'],
                             params['hunter_y'],
                             params['hunter_heading'])

        tolerance = params['tolerance_ratio'] * target.distance
        max_speed = params['speed_ratio'] * params['target_speed']
        other_info = None
        steps = 0

        random.seed(GLOBAL_SEEDS[params['part']])

        try:
            while steps < params['max_steps']:
                hunter_pos = (hunter.x, hunter.y)
                target_pos = (target.x, target.y)

                separation = self.distance(hunter_pos, target_pos)
                if separation < tolerance:
                    self.robot_found.put(True)
                    self.robot_steps.put(steps)
                    return

                target_meas = target.sense()
                turn, dist, other_info = next_move(hunter_pos, hunter.heading, target_meas, max_speed, other_info)

                dist = min(dist, max_speed)
                dist = max(dist, 0)
                turn = self.truncate_angle(turn)

                hunter.move(turn, dist)
                target.move_in_polygon()

                steps += 1

            self.robot_found.put(False)
            self.robot_steps.put(steps)

        except:
            self.robot_error.put(traceback.format_exc())


NOT_FOUND = "Part {} - Test Case {}: robot took {} step(s) which exceeded the {} allowable step(s)."


class CaseRunner(unittest.TestCase):
    """Run test case using specified parameters.

    Attributes:
        simulator(RunawaySimulator): Simulation.
    """
    @classmethod
    def setUpClass(cls):
        """Setup test class.
        """
        cls.simulator = RunawaySimulator()

    def run_with_params(self, k, test_params, test_method, student_method):
        """Run test case with parameters.

        Args:
            k(int): Test case global parameters.
            test_params(dict): Test parameters.
            test_method(func): Test function.
            student_method(func): Student submission function.
        """
        test_params.update(GLOBAL_PARAMETERS[k])

        test_process = mproc.Process(target=test_method, args=(student_method, test_params))

        error_message = ''
        steps = None
        robot_found = False

        try:
            test_process.start()
            test_process.join(TIME_LIMIT)
        except Exception as exp:
            error_message += exp.message + ' '

        if test_process.is_alive():
            test_process.terminate()
            error_message = ('Test aborted due to timeout. ' +
                             'Test was expected to finish in fewer than {} second(s).'.format(TIME_LIMIT))

        else:
            if not self.simulator.robot_error.empty():
                error_message += self.simulator.robot_error.get()

            if not self.simulator.robot_found.empty():
                robot_found = self.simulator.robot_found.get()

            if not self.simulator.robot_steps.empty():
                steps = self.simulator.robot_steps.get()

        self.assertFalse(error_message, error_message)
        self.assertTrue(robot_found, NOT_FOUND.format(test_params['part'],
                                                      test_params['test_case'],
                                                      steps,
                                                      test_params['max_steps']))


class Part1TestCase(CaseRunner):
    """Test Part 1

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """
    def setUp(self):
        """Setup for each test case.
        """
        self.test_method = self.simulator.simulate_without_hunter
        self.student_method = studentMain1.estimate_next_pos

        self.params = dict()
        self.params['tolerance_ratio'] = 0.02
        self.params['part'] = 1
        self.params['max_steps'] = 10
        self.params['noise_ratio'] = 0.00

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


class Part2TestCase(CaseRunner):
    """Test Part 2

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """
    def setUp(self):
        """Setup for each test case.
        """
        self.test_method = self.simulator.simulate_without_hunter
        self.student_method = studentMain2.estimate_next_pos

        self.params = dict()
        self.params['part'] = 2
        self.params['tolerance_ratio'] = 0.02
        self.params['max_steps'] = 1000
        self.params['noise_ratio'] = 0.05

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


class Part3TestCase(CaseRunner):
    """Test Part 3

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """
    def setUp(self):
        """Setup for each test case.
        """
        self.test_method = self.simulator.simulate_with_hunter
        self.student_method = studentMain3.next_move

        self.params = dict()
        self.params['part'] = 3
        self.params['tolerance_ratio'] = 0.02
        self.params['max_steps'] = 1000
        self.params['noise_ratio'] = 0.05
        self.params['speed_ratio'] = 2.00

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


class Part4TestCase(CaseRunner):
    """Test Part 1

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """
    def setUp(self):
        """Setup for each test case.
        """
        self.test_method = self.simulator.simulate_with_hunter
        self.student_method = studentMain4.next_move

        self.params = dict()
        self.params['part'] = 4
        self.params['tolerance_ratio'] = 0.02
        self.params['max_steps'] = 1000
        self.params['noise_ratio'] = 0.05
        self.params['speed_ratio'] = 0.99

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


# Only run all of the test automatically if this file was executed from the command line.
# Otherwise, let Nose/py.test do it's own thing with the test cases.
if __name__ == "__main__":
    suites = map(lambda case: unittest.TestSuite(unittest.TestLoader().loadTestsFromTestCase(case)),
                 [Part1TestCase, Part2TestCase, Part3TestCase, Part4TestCase])

    total_passes = 0

    for i, suite in zip(range(1, 1+len(suites)), suites):
        print "====================\nTests for Part {}:".format(i)

        result = unittest.TestResult()
        suite.run(result)

        for x in result.errors:
            print x[0], x[1]
        for x in result.failures:
            print x[0], x[1]

        num_errors = len(result.errors)
        num_fails = len(result.failures)
        num_passes = result.testsRun - num_errors - num_fails
        total_passes += num_passes

        print "Successes: {}\nFailures: {}\n".format(num_passes, num_errors + num_fails)

    print "====================\nOverall Score: {}".format(total_passes * CREDIT_PER_PASS)
