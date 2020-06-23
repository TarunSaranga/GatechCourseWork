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
#        print("Measurements:")
#        print(measurements)
#        print("")
        for beacon in measurements:
            if(measurements[beacon]['type'] == 'beacon'):
                if(beacon not in self.beaconids):
                    self.beaconids.append(beacon)
            elif(measurements[beacon]['type'] == 'site'):
                if(beacon not in self.siteids):
                    self.siteids.append(beacon)
#        print("Beaconids:")
#        print(self.beaconids)
#        print("")
        nBeacons = len(self.beaconids)
        
        ## Expand Omega and Xi to for new beacons | Create Omega and Xi for first time using init
        if(self.init):
            self.init = 0
#            print("Initial setup")
#            print("")
            
            self.dim = (1 + nBeacons)*2
#            print("Initial Dimension (dim):")
#            print(self.dim)
#            print("")
            self.Omega.zero(self.dim, self.dim)
            self.Omega.value[0][0] = 1.0
            self.Omega.value[1][1] = 1.0   
#            print("Initial Omega:")
#            for i in range(self.Omega.dimx):
#                print(self.Omega[i])
#            print("")
            
            self.Xi.zero(self.dim,1)
            self.Xi.value[0][0] = 0
            self.Xi.value[1][0] = 0
#            print("Initial Xi:")
#            for i in range(self.Xi.dimx):
#                print(self.Xi[i])
#            print("")
        
        elif(nBeacons > ((self.dim/2) - 1)):
#            print("New beacons setup")
#            print("")
            nNewBeacons = nBeacons - ((self.dim/2) - 1)
#            print("New beacons no=")
#            print(nNewBeacons)
            assignment_list = range(self.dim)
            self.dim = (1 + nBeacons)*2
            self.Omega = self.Omega.expand(self.dim, self.dim, assignment_list)
#            print("After New_Beacons Omega:")
#            for i in range(self.Omega.dimx):
#                print(self.Omega[i])
#            print("")
            self.Xi = self.Xi.expand(self.dim, 1, assignment_list, [0])
#            print("After New_Beacons Xi:")
#            for i in range(self.Xi.dimx):
#                print(self.Xi[i])
#            print("")
            
        ## for each beacon modify the slam 
        
        for beacon in self.beaconids:
            
#            print("beaconid")
#            print(beacon)
#            print("")
            if(beacon in measurements):
                dist = measurements[beacon]['distance']
#                print("distance")
#                print(dist)
#                print("")
                bearing = measurements[beacon]['bearing']
#                print("bearing")
#                print(bearing)
#                print("")
                
                ## Decode the measurement into [x,y] coordinates
                dx = dist * math.cos(bearing + self.bearing)
                dy = dist * math.sin(bearing + self.bearing)
                
                measurement = [self.beaconids.index(beacon), dx, dy]
#                print("measurement of beacon")
#                print(measurement)
#                print("")
                
                ## update Omega and Xi using the Online Slam measurement part
                m = 2 * ( 1 + measurement[0])
                
                for b in range(2):
                    self.Omega.value[b  ][b  ] += 1.0 / self.measurement_noise
                    self.Omega.value[m+b][m+b] += 1.0 / self.measurement_noise
                    self.Omega.value[m+b][b  ] += -1.0 / self.measurement_noise
                    self.Omega.value[b  ][m+b] += -1.0 / self.measurement_noise
                    
                    self.Xi.value[b  ][0] += -measurement[1+b] / self.measurement_noise
                    self.Xi.value[m+b][0] += measurement[1+b] / self.measurement_noise
                
#                print("Updated Omega:")
#                for i in range(self.Omega.dimx):
#                    print(self.Omega[i])
#                print("")
                
#                print("Updated Xi:")
#                for i in range(self.Xi.dimx):
#                    print(self.Xi[i])
#                print("")
            else:
#                print("No beacon Information")
                pass
            
        mu = self.Omega.inverse() * self.Xi
    
        x = mu[0][0]
        y = mu[1][0]
        self.curr_pos = [x,y]
        return x, y
    
    def truncate_angle(self,t):
        return ((t+ math.pi) % (2* math.pi)) - math.pi
    
    def process_movement(self, steering, distance, motion_noise=1.0):
        """Process a new movement.

        Args:
            steering(float): amount to turn
            distance(float): distance to move
            motion_noise(float): movement noise

        Returns:
            x, y: current belief in location of the rover relative to initial location after movement
        """
        ang = self.bearing + float(steering)
#        print("ang")
#        print(ang)
        bearing = self.truncate_angle(ang)
        self.bearing = bearing
        dx = (distance * math.cos(bearing))
        dy = (distance * math.sin(bearing))
        
        motion = [dx,dy]
        n = 2
        
        assignment_list = [0,1] + range(4, self.dim+2)
        self.Omega = self.Omega.expand(self.dim+2, self.dim+2, assignment_list)
#        print("OS_expanded_Omega:")
#        for i in range(self.Omega.dimx):
#            print(self.Omega[i])
#        print("")
        self.Xi = self.Xi.expand(self.dim+2, 1, assignment_list, [0])
#        print("OS_expanded_Xi:")
#        for i in range(self.Xi.dimx):
#            print(self.Xi[i])
#        print("")
        
        for b in range(4):
            self.Omega.value[b][b] += 1.0 / motion_noise
        for b in range(2):
            self.Omega.value[b  ][n+b] += -1.0 / motion_noise
            self.Omega.value[n+b][b  ] += -1.0 / motion_noise
            self.Xi.value[b  ][0] += -motion[b] / motion_noise
            self.Xi.value[n+b][0] += motion[b] / motion_noise
        
#        print("after_motion_Omega:")
#        for i in range(self.Omega.dimx):
#            print(self.Omega[i])
#        print("")
#        print("after_motion_Xi:")
#        for i in range(self.Xi.dimx):
#            print(self.Xi[i])
#        print("")
        
        Omega_prime = self.Omega.take(range(2, self.dim+2), range(2, self.dim+2))
#        print("OmegaPrime:")
#        for i in range(Omega_prime.dimx):
#            print(Omega_prime[i])
#        print("")
        Xi_prime = self.Xi.take(range(2, self.dim+2), [0])
        A = self.Omega.take([0,1], range(2, self.dim+2))
        B = self.Omega.take([0,1], [0,1])
        C = self.Xi.take([0,1], [0])

        self.Omega = Omega_prime - A.transpose() * B.inverse() * A
        self.Xi = Xi_prime - A.transpose() * B.inverse() * C
        
#        print("after_OS_Omega:")
#        for i in range(self.Omega.dimx):
#            print(self.Omega[i])
#        print("")
#        print("after_OS_Xi:")
#        for i in range(self.Xi.dimx):
#            print(self.Xi[i])
#        print("")
        
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
        self.tar_distance = 0.0
        self.tar_bearing = 0.0
        self.OS = SLAM()
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
        print("Measurements")
        print(measurements)
        print("")
        self.x , self.y = self.OS.process_measurements(measurements)
        print("Before moving")
        print("X: ",self.x," Y: ",self.y," hdg: ",self.OS.bearing,self.OS.bearing*180/math.pi )
        print("")
        if(len(self.OS.siteids)>0):
            print("SiteIds:")
            print(self.OS.siteids)
            print("")
            self.nearest_siteid = self.OS.siteids[0]
            min_dist = 100
            for siteid in self.OS.siteids:
                print("siteID:",siteid)
                if(siteid in measurements):
                    dist = measurements[siteid]['distance']
                    print("Distance:",dist)
                    if(dist < min_dist):
                        min_dist = dist
                        self.nearest_siteid = siteid
            
            if(self.nearest_siteid in measurements):
                distance_to_site = measurements[self.nearest_siteid]['distance']
                self.tar_distance = distance_to_site
                print("distance_to_site:",distance_to_site)
                print("")
                bearing_to_site = measurements[self.nearest_siteid]['bearing']
                self.tar_bearing = bearing_to_site
                print("bearing_to_site",bearing_to_site,  bearing_to_site*180/math.pi)
                print("")
            else:
                distance_to_site = self.tar_distance
                print("distance_to_site:",distance_to_site)
                print("")
                bearing_to_site = self.tar_bearing
                print("bearing_to_site",bearing_to_site, bearing_to_site*180/math.pi)
                print("")
                
            steering = self.OS.truncate_angle(bearing_to_site - self.OS.bearing)
            
            steering = max(-self.max_steering, steering)
            steering = min(self.max_steering, steering)
        
            if(distance_to_site < self.max_distance):
                distance = distance_to_site
            else:
                distance = self.max_distance
            
            self.x , self.y = self.OS.process_movement(steering,distance)
            print("After moving")
            print("X: ",self.x," Y: ",self.y," hdg: ",self.OS.bearing, self.OS.bearing*180/math.pi)
            print("")
            action = 'move ' + str(steering) + ' ' + str(distance)

        return action

