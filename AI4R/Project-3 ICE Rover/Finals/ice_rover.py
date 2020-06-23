"""
 === Introduction ===
 
   A few months ago a new rover was sent to McMurdo Station in the Antarctic. The rover is a technical marvel
   as it is equipped with the latest scientific sensors and analyzers capable of surviving the harsh climate of the
   South Pole.  The goal is for the rover to reach a series of test sites and perform scientific sampling and analysis.
   Due to the extreme conditions, the rover will be air dropped via parachute into the test area.  The good news is
   the surface is smooth and free from any type of obstacles, the bad news is the surface is entirely ice which may 
   introduce noise into your rovers movements.  The station scientists are ready to deploy the new rover, but first 
   we need to create and test the planning software that will be used on board to ensure it can complete it's goals.

   The assignment is broken up into two parts.

   Part A:
        Create a SLAM implementation to process a series of landmark (beacon) measurements and movement updates.

        Hint: A planner with an unknown number of motions works well with an online version of SLAM.

    Part B:
        Here you will create the planner for the rover.  The rover does unfortunately has a series of limitations:

        - Start position
          - The rover will land somewhere within range of at least 3 or more beacon for measurements.

        - Measurements
          - Measurements will come from beacons and test sites within range of the rover's antenna horizon.
            * The format is {'landmark id':{'distance':0.0, 'bearing':0.0, 'type':'beacon'}, ...}
          - Satellites and test sites will always return a measurement if in range.

        - Movements
          - Action: 'move 1.570963 1.0'
            * The rover will turn counterclockwise 90 degrees and then move 1.0
          - stochastic due to the icy surface.
          - if max distance or steering is exceeded, the rover will not move.

        - Samples
          - Provided as list of x and y coordinates, [[0., 0.], [1., -3.5], ...]
          - Action: 'sample'
            * The rover will attempt to take a sample at the current location.
          - A rover can only take a sample once per requested site.
          - The rover must be with 0.25 distance to successfully take a sample.
            * Hint: Be sure to account for floating point limitations
          - The is a 100ms penalty if the robot is requested to sample a site not on the list or if the site has
            previously been sampled.
          - Use sys.stdout = open('stdout.txt', 'w') to directly print data if necessary.         

        The rover will always execute a measurement first, followed by an action.

        The rover will have a time limit of 5 seconds to find and sample all required sites.
"""

import matrix
import math
import random
import copy

class SLAM:
    """Create a basic SLAM module.
    """
    def __init__(self):
        """Initialize SLAM components here.
        """
        self.measurement_noise = 1.0
        self.Omega = matrix.matrix()
        self.Xi = matrix.matrix()
        self.init = 1
        self.beaconids = []
        self.siteids = []
        self.dim = 0
        self.curr_pos = [0,0]
        self.bearing = 0.0

    def process_measurements(self, measurements):
        """Process a new series of measurements.

        Args:
            measurements(dict): Collection of measurements
                in the format {'landmark id':{'distance':0.0, 'bearing':0.0, 'type':'beacon'}, ...}

        Returns:
            x, y: current belief in location of the rover relative to initial location before movement
        """
        ## Identify beacons and get new beacons | Store beacon IDs in a list

        for beacon in measurements:
            if(beacon not in self.beaconids):
                self.beaconids.append(beacon)
            elif(measurements[beacon]['type'] == 'site'):
                if(beacon not in self.siteids):
                    self.siteids.append(beacon)

        nBeacons = len(self.beaconids)
        
        ## Expand Omega and Xi to for new beacons | Create Omega and Xi for first time using init
        if(self.init):
            self.init = 0           
 
            self.dim = (1 + nBeacons)*2

            self.Omega.zero(self.dim, self.dim)
            self.Omega.value[0][0] = 1.0
            self.Omega.value[1][1] = 1.0   

            
            self.Xi.zero(self.dim,1)
            self.Xi.value[0][0] = 0
            self.Xi.value[1][0] = 0

        
        elif(nBeacons > ((self.dim/2) - 1)):

            assignment_list = range(self.dim)
            self.dim = (1 + nBeacons)*2
            self.Omega = self.Omega.expand(self.dim, self.dim, assignment_list)

            self.Xi = self.Xi.expand(self.dim, 1, assignment_list, [0])

            
        ## for each beacon modify the slam 
        
        for beacon in self.beaconids:
            
            if(beacon in measurements):
                dist = measurements[beacon]['distance']
                bearing = measurements[beacon]['bearing']
                
                distance_sigma = 0.05*dist
                bearing_sigma = 0.02*dist
                self.measurement_noise = distance_sigma + bearing_sigma
                if(self.measurement_noise == 0):
                    self.measurement_noise = 1.0
                ## Decode the measurement into [x,y] coordinates
                dx = dist * math.cos(bearing + self.bearing)
                dy = dist * math.sin(bearing + self.bearing)
                
                measurement = [self.beaconids.index(beacon), dx, dy]

                
                ## update Omega and Xi using the Online Slam measurement part
                m = 2 * ( 1 + measurement[0])
                
                for b in range(2):
                    self.Omega.value[b  ][b  ] += 1.0 / self.measurement_noise
                    self.Omega.value[m+b][m+b] += 1.0 / self.measurement_noise
                    self.Omega.value[m+b][b  ] += -1.0  / self.measurement_noise
                    self.Omega.value[b  ][m+b] += -1.0 / self.measurement_noise
                    
                    self.Xi.value[b  ][0] += -measurement[1+b] / self.measurement_noise
                    self.Xi.value[m+b][0] += measurement[1+b] / self.measurement_noise

            else:
                pass
            
        mu = self.Omega.inverse() * self.Xi
    
        x = mu[0][0]
        y = mu[1][0]
        self.curr_pos = [x,y]
        return x, y
    
    def truncate_angle(self,t):
        return ((t+ math.pi) % (2* math.pi)) - math.pi
    
    def process_movement(self, steering, distance, motion_noise= 10):
        """Process a new movement.

        Args:
            steering(float): amount to turn
            distance(float): distance to move
            motion_noise(float): movement noise

        Returns:
            x, y: current belief in location of the rover relative to initial location after movement
        """
        ang = self.bearing + float(steering)
        bearing = self.truncate_angle(ang)
        self.bearing = bearing
        dx = (distance * math.cos(bearing))
        dy = (distance * math.sin(bearing))
        
        motion = [dx,dy]
        n = 2
        
        assignment_list = [0,1] + range(4, self.dim+2)
        self.Omega = self.Omega.expand(self.dim+2, self.dim+2, assignment_list)
        self.Xi = self.Xi.expand(self.dim+2, 1, assignment_list, [0])
        
        for b in range(4):
            self.Omega.value[b][b] += 1.0 #/ motion_noise
        for b in range(2):
            self.Omega.value[b  ][n+b] += -1.0 #/ motion_noise
            self.Omega.value[n+b][b  ] += -1.0 #/ motion_noise
            self.Xi.value[b  ][0] += -motion[b] #/ motion_noise
            self.Xi.value[n+b][0] += motion[b] #/ motion_noise
        
       
        Omega_prime = self.Omega.take(range(2, self.dim+2), range(2, self.dim+2))

        Xi_prime = self.Xi.take(range(2, self.dim+2), [0])
        A = self.Omega.take([0,1], range(2, self.dim+2))
        B = self.Omega.take([0,1], [0,1])
        C = self.Xi.take([0,1], [0])

        self.Omega = Omega_prime - A.transpose() * B.inverse() * A
        self.Xi = Xi_prime - A.transpose() * B.inverse() * C
        
       
        mu = self.Omega.inverse() * self.Xi
        
        x = mu[0][0]
        y = mu[1][0]
        
        self.curr_pos = [x,y]
        
        return x, y


class WayPointPlanner:
    """Create a planner to navigate the rover to reach all the intended way points from an unknown start position.
    """
    def __init__(self,  max_distance, max_steering):
        """Initialize your planner here.

        Args:
            max_distance(float): the max distance the robot can travel in a single move.
            max_steering(float): the max steering angle the robot can turn in a single move.
        """
        self.max_distance = max_distance
        self.max_steering = max_steering
        self.nearest_siteid = 0
        self.x = 0.0
        self.y = 0.0
        self.rel_x = 0.0
        self.rel_y = 0.0
        self.tar_distance = 2
        self.tar_bearing = math.pi/4
        self.rel_target_x = 0.0
        self.rel_target_y = 0.0
        self.OS = SLAM()
        self.abs_samp_sites = []
        self.init = 1
        self.sam_one = 0
    
    def measure_distance_and_bearing_to(self, point, noise=False):
        
        current_position = (self.x, self.y)

        distance_to_point = self.compute_distance(current_position, point)
        bearing_to_point = self.compute_bearing(current_position, point)

        if noise:
            distance_sigma = 0.05*distance_to_point
            bearing_sigma = 0.02*distance_to_point

            distance_noise = random.gauss(0, distance_sigma)
            bearing_noise = random.gauss(0, bearing_sigma)
        else:
            distance_noise = 0
            bearing_noise = 0

        measured_distance = distance_to_point + distance_noise
        measured_bearing = self.OS.truncate_angle(bearing_to_point - self.OS.bearing + bearing_noise)

        return (measured_distance, measured_bearing)

    
    def compute_bearing(self,p, q):
        x1, y1 = p
        x2, y2 = q
    
        dx = x2 - x1
        dy = y2 - y1
    
        return math.atan2(dy, dx)
    
    def compute_distance(self,p, q):
        x1, y1 = p
        x2, y2 = q
    
        dx = x2 - x1
        dy = y2 - y1
    
        return math.sqrt(dx**2 + dy**2)
        
    def next_move(self, sample_todo, measurements):
        """Next move based on the current set of measurements.

        Args:
            sample_todo(list): Set of locations remaining still needing a sample to be taken.
            measurements(dict): Collection of measurements from beacons and test sites in range.
                in the format {'landmark id':{'distance':0.0, 'bearing':0.0, 'type':'beacon'}, ...}

        Return:
            Next command to execute on the rover.
                allowed:
                    'move 1.570963 1.0' - turn left 90 degrees and move 1.0 distance
                    'sample' - take sample (will succeed if within tolerance of intended sample site)
        """
        action = 'move ' + str(0.0) + ' ' + str(0.0)
        if(self.init == 1):
            self.abs_samp_sites = copy.copy(sample_todo)
            action = 'move ' + str(0.0) + ' ' + str(0.0)
            self.init = 0

        if(self.sam_one == 0):
            self.x , self.y = self.OS.process_measurements(measurements)

            
            if(len(self.OS.siteids)>0):

                self.nearest_siteid = self.OS.siteids[0]
                min_dist = 100
                for siteid in self.OS.siteids:

                    if(siteid in measurements):
                        dist = measurements[siteid]['distance']
                        if(dist < min_dist):
                            min_dist = dist
                            self.nearest_siteid = siteid
                
                if(self.nearest_siteid in measurements):
                    distance_to_site = measurements[self.nearest_siteid]['distance']
                    self.tar_distance = distance_to_site

                    bearing_to_site = measurements[self.nearest_siteid]['bearing']
                    self.tar_bearing = bearing_to_site
                    
                else:
                    distance_to_site = self.tar_distance
                    bearing_to_site = self.tar_bearing

                    
                    
                steering = bearing_to_site
                
                steering = max(-self.max_steering, steering)
                steering = min(self.max_steering, steering)
                
               
                if(steering < 0.1 and steering > -0.1):
                    if(distance_to_site < self.max_distance):
                        distance = distance_to_site
                    else:
                        distance = self.max_distance
                else:
                    distance = 0
                
                if(distance_to_site > 0.15):
                    self.x , self.y = self.OS.process_movement(steering,distance)

                    action = 'move ' + str(steering) + ' ' + str(distance)
                elif(distance_to_site < 0.15):
                    action = 'sample'
                    self.sam_one = 1
        
        elif(self.sam_one == 1):
            current_site = list(set(self.abs_samp_sites) - set(sample_todo))
            abs_x = current_site[0][0]
            abs_y = current_site[0][1]

            self.rel_x = abs_x - self.x
            self.rel_y = abs_y - self.y
            self.sam_one = 2
            
            abs_target_x, abs_target_y = sample_todo[0]
            self.rel_target_x = abs_target_x - self.rel_x
            self.rel_target_y = abs_target_y - self.rel_y
            
            action = 'move ' + str(0.0) + ' ' + str(0.0)
            
        elif(self.sam_one == 2):
            target_point = [self.rel_target_x, self.rel_target_y]
            self.tar_distance, self.tar_bearing = self.measure_distance_and_bearing_to(target_point)
            
            self.x , self.y = self.OS.process_measurements(measurements)
            
            distance_to_site = self.tar_distance
            bearing_to_site = self.tar_bearing
                 
            steering = bearing_to_site
                
            steering = max(-self.max_steering, steering)
            steering = min(self.max_steering, steering)

            if(steering < 0.1 and steering > -0.1):
                if(distance_to_site < self.max_distance):
                    distance = distance_to_site
                else:
                    distance = self.max_distance
            else:
                distance = 0
            
            if(distance_to_site > 0.15):
                self.x , self.y = self.OS.process_movement(steering,distance)
                action = 'move ' + str(steering) + ' ' + str(distance)
                
            elif(distance_to_site < 0.15):
                action = 'sample'
                self.sam_one = 1
                
            
        return action

