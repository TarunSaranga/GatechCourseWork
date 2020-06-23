"""
=== Introduction ===

In this problem, you will again build a planner that helps a robot
  find the best path through a warehouse filled with boxes
  that it has to pick up and deliver to a dropzone. Unlike Part A,
  however, in this problem the robot is moving in a continuous world
  (albeit in discrete time steps) and has constraints on the amount
  it can turn its wheels in a given time step.

Your file must be called `partB.py` and must have a class
  called `DeliveryPlanner`.
This class must have an `__init__` function that takes five 
  arguments: `self`, `warehouse`, `todo`, `max_distance`, and
  `max_steering`.
The class must also have a function called `plan_delivery` that 
  takes a single argument, `self`.

=== Input Specifications ===

`warehouse` will be a list of m strings, each with n characters,
  corresponding to the layout of the warehouse. The warehouse is an
  m x n grid. warehouse[i][j] corresponds to the spot in the ith row
  and jth column of the warehouse, where the 0th row is the northern
  end of the warehouse and the 0th column is the western end.

The characters in each string will be one of the following:

'.' (period) : traversable space.
'' (hash) : a wall. If the robot contacts a wall space, it will crash.
'@' (dropzone): the space where all boxes must be delivered. The dropzone may be traversed like 
  a '.' space.

Each space is a 1 x 1 block. The upper-left corner of space warehouse[i][j] is at the point (j,-i) in
  the plane. Spaces outside the warehouse are considered walls; if any part of the robot leaves the 
  warehouse, it will be considered to have crashed into the exterior wall of the warehouse.

For example, 
  warehouse = ['..',
               '..',
               '..@']
  is a 3x3 warehouse. The dropzone is at space (2,-2) and there are walls at spaces (1,0) 
  and (1,-1). The rest of the warehouse is empty space.

The robot is a circle of radius 0.25. The robot begins centered in the dropzone space.
  The robot's initial bearing is 0.

The argument `todo` is a list of points representing the center point of each box.
  todo[0] is the first box which must be delivered, followed by todo[1], and so on.
  Each box is a square of size 0.2 x 0.2. If the robot contacts a box, it will crash.

The arguments `max_distance` and `max_steering` are parameters constraining the movement
  of the robot on a given time step. They are described more below.

=== Rules for Movement ===

- The robot may move any distance between 0 and `max_distance` per time step.
- The robot may set its steering angle anywhere between -`max_steering` and 
  `max_steering` per time step. A steering angle of 0 means that the robot will
  move according to its current bearing. A positive angle means the robot will 
  turn counterclockwise by `steering_angle` radians; a negative steering_angle 
  means the robot will turn clockwise by abs(steering_angle) radians.
- Upon a movement, the robot will change its steering angle instantaneously to the 
  amount indicated by the move, and then it will move a distance in a straight line in its
  new bearing according to the amount indicated move.
- The cost per move is 1 plus the amount of distance traversed by the robot on that move.

- The robot may pick up a box whose center point is within 0.5 units of the robot's center point.
- If the robot picks up a box, it incurs a total cost of 2 for that move (this already includes 
  the 1-per-move cost incurred by the robot).
- While holding a box, the robot may not pick up another box.
- The robot may put a box down at a total cost of 1.5 for that move. The box must be placed so that:
  - The box is not contacting any walls, the exterior of the warehouse, any other boxes, or the robot
  - The box's center point is within 0.5 units of the robot's center point
- A box is always oriented so that two of its edges are horizontal and the other two are vertical.
- If a box is placed entirely within the '@' space, it is considered delivered and is removed from the 
  warehouse.
- The warehouse will be arranged so that it is always possible for the robot to move to the 
  next box on the todo list without having to rearrange any other boxes.

- If the robot crashes, it will stop moving and incur a cost of 100*distance, where distance
  is the length it attempted to move that move. (The regular movement cost will not apply.)
- If an illegal move is attempted, the robot will not move, but the standard cost will be incurred.
  Illegal moves include (but are not necessarily limited to):
    - picking up a box that doesn't exist or is too far away
    - picking up a box while already holding one
    - putting down a box too far away or so that it's touching a wall, the warehouse exterior, 
      another box, or the robot
    - putting down a box while not holding a box

=== Output Specifications ===

`plan_delivery` should return a LIST of strings, each in one of the following formats.

'move {steering} {distance}', where '{steering}' is a floating-point number between
  -`max_steering` and `max_steering` (inclusive) and '{distance}' is a floating-point
  number between 0 and `max_distance`

'lift {b}', where '{b}' is replaced by the index in the list `todo` of the box being picked up
  (so if you intend to lift box 0, you would return the string 'lift 0')

'down {x} {y}', where '{x}' is replaced by the x-coordinate of the center point of where the box
  will be placed and where '{y}' is replaced by the y-coordinate of that center point
  (for example, 'down 1.5 -2.9' means to place the box held by the robot so that its center point
  is (1.5,-2.9)).

=== Grading ===

- Your planner will be graded against a set of test cases, each equally weighted.
- Each task will have a "baseline" cost. If your set of moves results in the task being completed
  with a total cost of K times the baseline cost, you will receive 1/K of the credit for the
  test case. (Note that if K < 1, this means you earn extra credit!)
- Otherwise, you will receive no credit for that test case. This could happen for one of several 
  reasons including (but not necessarily limited to):
  - plan_delivery's moves do not deliver the boxes in the correct order.
  - plan_delivery's output is not a list of strings in the prescribed format.
  - plan_delivery does not return an output within the prescribed time limit.
  - Your code raises an exception.

=== Additional Info ===

- You may add additional classes and functions as needed provided they are all in the file `partB.py`.
- Your partB.py file must not execute any code when it is imported. 
- Upload partB.py to Project 2 on T-Square in the Assignments section. Do not put it into an 
  archive with other files.
- Ask any questions about the directions or specifications on Piazza.
"""
import robot
import math
import copy
class DeliveryPlanner:

    def __init__(self, warehouse, todo, max_distance, max_steering):

        # TODO: You may use this function for any initialization required for your planner
        self.warehouse = warehouse
        self.todo = todo
        self.max_distance = max_distance
        self.max_steering = max_steering

    def plan_delivery(self):
        
        ## Make the Grid world with 20x20 resolution
        #print "Height of the warehouse:",len(self.warehouse)
        #print "Width of the warehouse:",len(self.warehouse[0])
        
#        print(" ")
#        print("inputWarehouse")
#        for i in range(len(self.warehouse)):
#            print(self.warehouse[i])
        
        grid_size = 10
        moves = []
        newWarehouse = [['.' for i in range(grid_size*len(self.warehouse[0]))] for j in range(grid_size*len(self.warehouse))]
        
        #print " "
        #print "newEmptytWarehouse"
        #for i in range(len(newWarehouse)):
        #    print newWarehouse[i]
        walls = []
        drop_zone = []
        for i in range(len(self.warehouse)):
            for j in range(len(self.warehouse[0])):
                if self.warehouse[i][j] == '#':
                    walls.append([i,j])
                elif self.warehouse[i][j] == '@':
                    drop_zone.append([i,j])
        
        packages = self.todo
        expanded_pkgs = []
        
        for pkg in packages:
            expanded_pkgs.append([abs(int(pkg[1]*grid_size)),int(pkg[0]*grid_size)])
            
        #print " "
        #print "packages at: ", expanded_pkgs
        #print " "
        #print "Walls at: ", walls
        
        #print " "
        #print "drop_zone at: ", drop_zone
        
        newWalls = []
        for wall in walls:
            for i in range(-int(0.3*grid_size),grid_size+int(0.3*grid_size)):
                for j in range(-int(0.3*grid_size),grid_size+int(0.3*grid_size)):
                    newWalls.append([(wall[0]*grid_size)+i,(wall[1]*grid_size)+j])
        
        new_drop_zone = []
        for drop in drop_zone:
            for i in range(0,grid_size):
                for j in range(0,grid_size):
                    new_drop_zone.append([(drop[0]*grid_size)+i,(drop[1]*grid_size)+j])
        #print " "
        #print "NewWalls at: ", newWalls
        robot_init_pos = [math.ceil((2*(drop_zone[0][0]*grid_size)+grid_size)/2),math.ceil((2*(drop_zone[0][1]*grid_size)+grid_size)/2)]
        #print " "
        #print "Robot initial position"
        #print robot_init_pos
        
        ## Wall padding
        for i in range(len(newWarehouse)):
            for j in range(len(newWarehouse[0])):
                if( (i<int(0.3*grid_size)) or (i >= len(newWarehouse) - int(0.3*grid_size))):
                    newWarehouse[i][j] = '#'
                if( (j<int(0.3*grid_size)) or (j >= len(newWarehouse[0]) - int(0.3*grid_size))):
                    newWarehouse[i][j] = '#'
        
                
        
        for i in range(len(newWarehouse)):
            for j in range(len(newWarehouse[0])):
                if([i,j] in newWalls):
                    newWarehouse[i][j] = '#'
                if([i,j] in new_drop_zone):
                    newWarehouse[i][j] = '@'
                if([i,j] == robot_init_pos):
                    newWarehouse[i][j] = '*'
                if([i,j] in expanded_pkgs):
                    for k in range(int(0.3*grid_size)):
                        for l in range(int(0.3*grid_size)):
                            newWarehouse[i][j] = '#'
                            newWarehouse[i][j+l] = '#'
                            newWarehouse[i+k][j] = '#'
                            newWarehouse[i+k][j+l] = '#'
                            newWarehouse[i-k][j+l] = '#'
                            newWarehouse[i+k][j-l] = '#'
                            newWarehouse[i][j-l] = '#'
                            newWarehouse[i-k][j] = '#'
                            newWarehouse[i-k][j-l] = '#'
                
        print(" ")
        print("ExpandedWarehouse")
        for i in range(len(newWarehouse)):
            print(newWarehouse[i])
            
        
        ## Movement Cost
        cost = 1
        delta = [[-1, 0 ], # go up
                 [ 0, -1], # go left
                 [ 1, 0 ], # go down
                 [ 0, 1 ], # go right
                 [-1, 1 ], # go top right
                 [-1, -1], # go top left
                 [ 1, 1 ], # go down right
                 [ 1, -1], # go down left
                 ]
        ## Helper Functions
        ## Heuristic Function
        def compute_heu(grid,goal,delta,cost):
            
            def inGrid(grid, x, y):
                if x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid):
                    return True
                else:
                    return False
            
            value = [[99999 for x in range(len(grid[0]))] for y in range(len(grid))]
            
            value[goal[0]][goal[1]] = 0
            openList = []
            openList.append([0, goal[0],goal[1]])
            while len(openList) != 0:
                openList.sort()
                currentCell = openList.pop(0)
                for i in range(len(delta)):
                    targetX = currentCell[2] + delta[i][1]
                    targetY = currentCell[1] + delta[i][0]
                    if inGrid(grid, targetX, targetY):
                        if (grid[targetY][targetX] == '.' or grid[targetY][targetX] == '@')  and value[targetY][targetX] == 99999:
                            openList.append([(currentCell[0]+ cost + int(3*distance_between(goal,[targetX,targetY]))), targetY, targetX])
                            value[targetY][targetX] = (currentCell[0] + cost + int(3*distance_between(goal,[targetX,targetY])))
                        
            return value
        ## Search Function
        def search(grid, init , goal, cost, heuristic, moves):


            closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
            for i in range(len(heuristic)):
                for j in range(len(heuristic)):
                    if(heuristic[i][j] == 99999):
                        closed[i][j] = 1
            #closed[init[0]][init[1]] = 1
            #for i in range(len(closed)):
            #    for j in range(len(closed[0])):
            #        if(closed[i][j] != 99999):
            #            closed[i][j] = 0
            #        else:
            #            closed[i][j] = 1
            

#            print(" ")
#            print("closed array in the beginning")
#            for i in range(len(closed[0])):
#                print((closed[i]))
            
            
            expand = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]
            for i in range(len(heuristic)):
                for j in range(len(heuristic)):
                    if(heuristic[i][j] == 99999):
                        expand[i][j] = -9
#            expand = copy.copy(heuristic)
#            for i in range(len(expand)):
#                for j in range(len(expand[0])):
#                    if(expand[i][j] != 99999):
#                        expand[i][j] = -1
#                    if(expand[i][j] == 0):
#                        expand[i][j] = -99
            #print(" ")
            #print("expand array in the beginning")
            #for i in range(len(expand[0])):
            #    print(expand[i])
            #action = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]

            x = init[0]
            y = init[1]
            g = 0
            f = g + heuristic[x][y]
            #print(" ")
            #print("heuristic array in the search")
            #for i in range(len(heuristic[0])):
            #    print(heuristic[i])
            open_cells = [[f, g, x, y]]
            #print("")
            #print("open_cells:")
            #print(open_cells)

            found = False  # flag that is set when search is complete
            resign = False # flag set if we can't find expand
            count = 0
            
            while not found and not resign:
                if len(open_cells) == 0:
                    resign = True
                    return moves
                else:
                    open_cells.sort()
                    open_cells.reverse()
                    next_cell = open_cells.pop()

                    #print("")
                    #print("Next_cell")
                    #print(next_cell)
                    x = next_cell[2]
                    y = next_cell[3]
                    g = next_cell[1]
                    f = next_cell[0]
                    expand[x][y] = count
                    if(count>0):
                        mv = 'move ' + str(x) +' '+ str(y)
                        moves.append(mv)
                    

                    count += 1
                    
                    if distance_between([x,y],[goal[0],goal[1]]) <= 0.45*grid_size or distance_between([x,y],[goal[0],goal[1]]) == math.sqrt((0.4*grid_size)**2 +(0.4*grid_size)**2):
                        found = True
                        print("")
                        print("expand")
                        for i in range(len(expand)):
                            print((expand[i]))
                        return moves
                    else:
                        for i in range(len(delta)):
                            x2 = x + delta[i][0]
                            y2 = y + delta[i][1]
                            if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                                if closed[x2][y2] == 0 and (grid[x2][y2] == '.' or grid[x2][y2] == '@') :
                                    g2 = g + cost
                                    f2 = g2 + heuristic[x2][y2]
                                    open_cells.append([f2, g2, x2, y2])
                                    #print("")
                                    #print("after appending open_cells")
                                    #print(open_cells)
                                    closed[x2][y2] = 1
                                
            print("")
            print("expand")
            for i in range(len(expand[0])):
                print((expand[i]))
            
            return moves
        
        def distance_between(a,b):
            i,j = a
            p,q = b
            dist = math.sqrt((i-p)**2 + (j-q)**2)
            return dist
        
        distances = []
        for to in range(len(expanded_pkgs)):
            ddd = distance_between([int(robot_init_pos[0]),int(robot_init_pos[0])],[int(expanded_pkgs[to][0]),int(expanded_pkgs[to][0])])
            distances.append([ddd,to])
        
        distances.sort(reverse=True)
        
        
        ## For each package
        for to in range(len(expanded_pkgs)):
            #pos = distances.pop()
            #to = pos[1]
            pkg_pos = expanded_pkgs[to]
            
            print(" ")
            print(("Package:",to))
            
            newWarehouse = [['.' for i in range(grid_size*len(self.warehouse[0]))] for j in range(grid_size*len(self.warehouse))]
            
            newWalls = []
            for wall in walls:
                for i in range(-int(0.3*grid_size),grid_size+int(0.3*grid_size)):
                    for j in range(-int(0.3*grid_size),grid_size+int(0.3*grid_size)):
                        newWalls.append([(wall[0]*grid_size)+i,(wall[1]*grid_size)+j])
            
            for i in range(len(newWarehouse)):
                for j in range(len(newWarehouse[0])):
                    if([i,j] in newWalls):
                        newWarehouse[i][j] = '#'
                    if([i,j] in new_drop_zone):
                        newWarehouse[i][j] = '@'
                    if([i,j] == robot_init_pos):
                        newWarehouse[i][j] = '*'
                    if([i,j]  not in [pkg_pos] and [i,j] in expanded_pkgs):
                        for k in range(int(0.3*grid_size)):
                            for l in range(int(0.3*grid_size)):
                                newWarehouse[i][j] = '#'
                                newWarehouse[i][j+l] = '#'
                                newWarehouse[i+k][j] = '#'
                                newWarehouse[i+k][j+l] = '#'
                                newWarehouse[i-k][j+l] = '#'
                                newWarehouse[i+k][j-l] = '#'
                                newWarehouse[i][j-l] = '#'
                                newWarehouse[i-k][j] = '#'
                                newWarehouse[i-k][j-l] = '#'
            
            ## Wall padding
            for i in range(len(newWarehouse)):
                for j in range(len(newWarehouse[0])):
                    if( (i<int(0.3*grid_size)) or (i >= len(newWarehouse) - int(0.3*grid_size))):
                        newWarehouse[i][j] = '#'
                    if( (j<int(0.3*grid_size)) or (j >= len(newWarehouse[0]) - int(0.3*grid_size))):
                        newWarehouse[i][j] = '#'
            
            print(" ")
            print("ExpandedWarehouse for package:",to)
            for i in range(len(newWarehouse)):
                print(newWarehouse[i])
            ## Move towards the package
            heu = compute_heu(newWarehouse, [int(pkg_pos[0]),int(pkg_pos[1])], delta, cost) 
            
#            print(" ")
#            print("Heuristic Grid")
#            for i in range(len(heu[0])):
#                print((heu[i]))
            
            if(to == 0):
                final_pos = [int(robot_init_pos[0]),int(robot_init_pos[1])]
            
            moves = search(newWarehouse, final_pos , [int(pkg_pos[0]),int(pkg_pos[1])], cost, copy.copy(heu), moves)
            
            ## Grab the package
            moves.append('lift ' + str(to))
            newWarehouse[int(pkg_pos[0])][int(pkg_pos[1])] = newWarehouse[int(pkg_pos[0])][int(pkg_pos[1])].replace('$','.')
            
            for i in range(len(moves)):
                mov = moves[-(i+1)].split()
                if(mov[0] == 'move'):
                        final_pos = int(mov[1]),int(mov[2])
                        break
            ## Move towards the drop_zone
            heu = compute_heu(newWarehouse, [int(robot_init_pos[0]),int(robot_init_pos[1])] , delta ,cost)
#            print(" ")
#            print("Heuristic Grid")
#            for i in range(len(heu[0])):
#                print((heu[i]))
            moves = search(newWarehouse, final_pos, [int(robot_init_pos[0]),int(robot_init_pos[1])], cost, heu, moves)
            ## Drop the Package
            moves.append('down ' + str(int(robot_init_pos[1])/grid_size)+' '+ str(int(robot_init_pos[0])/grid_size))
            for i in range(len(moves)):
                    mov = moves[-(i+1)].split()
                    if(mov[0] == 'move'):
                            final_pos = int(mov[1]),int(mov[2])
                            break
        
        print(moves)
        cal_moves = []
        def truncate_angle(t):
            return ((t+PI) % (2*PI)) - PI
        myrobot = robot.Robot(x=robot_init_pos[1]/grid_size, y=-robot_init_pos[0]/grid_size, bearing=0.0, max_distance=self.max_distance, max_steering=self.max_steering)
        myrobot.set_noise( steering_noise=0, distance_noise=0, measurement_noise=0)
        #print("Robot's init pos:",myrobot)
        robot_pos = myrobot.__repr__()
        for move in moves:
            mv = move.split()
            if(mv[0] == 'lift'):
                cal_moves.append(move)
            if(mv[0] == 'down'):
                cal_moves.append(move)
            if(mv[0] == 'move'):
                x,y = float(mv[2])/grid_size, -float(mv[1])/grid_size
                #print("x=",x,"y=",y)
                dist, bearing = myrobot.measure_distance_and_bearing_to([x,y])
                target_bearing = myrobot.bearing + bearing
                steer = robot.truncate_angle(target_bearing - myrobot.bearing)
                
                steer = max(-self.max_steering, steer)
                steer = min(self.max_steering, steer)
                
                while(steer>0.0000000000000006 or steer < -0.0000000000000006):
                    steer = robot.truncate_angle(target_bearing - myrobot.bearing)
                    #print("steer",steer)
                    steer = max(-self.max_steering, steer)
                    steer = min(self.max_steering, steer)
                    m = "move " + str(steer) + " " + str(0)
                    cal_moves.append(m)
                    myrobot.move(steer,0)
                    #print("robot bearing",myrobot.bearing)
                    #print("target bearing",target_bearing)
                
                while(dist > 0.0000001):
                    dist,bearing = myrobot.measure_distance_and_bearing_to([x,y])
                    dist = max(0, dist)
                    dist = min(self.max_distance, dist)
                    #print("Distance to point",dist)
                    m = "move " + str(0) + " " + str(dist)
                    cal_moves.append(m)
                    myrobot.move(0,dist)
                    #print("robot position",myrobot.__repr__(),"Robot bearing:",myrobot.bearing)
                    #print("target position",[x,y])
                    
#                    m = "move " + str(steer) + " " + str(dist)
#                    cal_moves.append(m)
#                    print("new dist:",dist,"new steer",steer)
#                    myrobot.move(steer,dist)
#                    print("new robot pos",myrobot)
#                    robot_pos = myrobot.__repr__()
        
        
        return cal_moves

warehouse= ['#######.',
            '#.......',
            '#@......']
todo = [(7.5, -1.5),
        (7.5, -0.5)]
max_distance = 5.0
max_steering = math.pi / 2. + 0.01
min_cost = 38.

planner = DeliveryPlanner(warehouse, todo, max_distance, max_steering)
cal_moves = planner.plan_delivery()

moves = ['move 1.570963 2.0',  # rotate and move north 2 spaces
                 'move 1.570963 0.1',  # rotate west and move closer to second box
                 'lift 1',             # lift the second box
                 'move 0.785398 1.5',  # rotate to sw and move down 1.5 squares
                 'down 3.5 -4.0',      # set the box out of the way
                 'move -0.785398 2.0', # rotate to west and move 2.5 squares
                 'move -1.570963 2.7', # rotate to north and move to pick up box 0
                 'lift 0',             # lift the first box
                 'move -1.570963 0.0', # rotate to the south east
                 'move -0.785398 1.0', # finish rotation
                 'move 0.785398 2.5',  # rotate to east and move
                 'move -1.570963 2.5', # rotate and move south
                 'down 4.5 -4.5',      # set down the box in the dropzone
                 'move -1.570963 0.6', # rotate to west and move towards box 1
                 'lift 1',             # lift the second box
                 'move 1.570963 0.0',  # rotate north
                 'move 1.570963 0.6',  # rotate east and move back towards dropzone
                 'down 4.5 -4.5']      # deliver second box

print(cal_moves)

#improved_whViz_partB.drawWH(warehouse, todo, cal_moves)
