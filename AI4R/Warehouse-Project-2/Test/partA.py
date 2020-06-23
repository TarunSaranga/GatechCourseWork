'''
=== Introduction ===

In this problem, you will build a planner that helps a robot
  find the best path through a warehouse filled with boxes
  that it has to pick up and deliver to a dropzone.

Your file must be called `partA.py` and must have a class
  called `DeliveryPlanner`.
This class must have an `__init__` function that takes three 
  arguments: `self`, `warehouse`, and `todo`.
The class must also have a function called `plan_delivery` that 
  takes a single argument, `self`.

=== Input Specifications ===

`warehouse` will be a list of m strings, each with n characters,
  corresponding to the layout of the warehouse. The warehouse is an
  m x n grid. warehouse[i][j] corresponds to the spot in the ith row
  and jth column of the warehouse, where the 0th row is the northern
  end of the warehouse and the 0th column is the western end.

The characters in each string will be one of the following:

'.' (period) : traversable space. The robot may enter from any adjacent space.
'#' (hash) : a wall. The robot cannot enter this space.
'@' (dropzone): the starting point for the robot and the space where all boxes must be delivered.
  The dropzone may be traversed like a '.' space.
[0-9a-zA-Z] (any alphanumeric character) : a box. At most one of each alphanumeric character 
  will be present in the warehouse (meaning there will be at most 62 boxes). A box may not
  be traversed, but if the robot is adjacent to the box, the robot can pick up the box.
  Once the box has been removed, the space functions as a '.' space.

For example, 
  warehouse = ['1#2',
               '.#.',
               '..@']
  is a 3x3 warehouse.
  - The dropzone is at the warehouse cell in row 2, column 2.
  - Box '1' is located in the warehouse cell in row 0, column 0.
  - Box '2' is located in the warehouse cell in row 0, column 2.
  - There are walls in the warehouse cells in row 0, column 1 and row 1, column 1.
  - The remaining five warehouse cells contain empty space.
#
The argument `todo` is a list of alphanumeric characters giving the order in which the 
  boxes must be delivered to the dropzone. For example, if 
  todo = ['1','2']
  is given with the above example `warehouse`, then the robot must first deliver box '1'
  to the dropzone, and then the robot must deliver box '2' to the dropzone.

=== Rules for Movement ===

- Two spaces are considered adjacent if they share an edge or a corner.
- The robot may move horizontally or vertically at a cost of 2 per move.
- The robot may move diagonally at a cost of 3 per move.
- The robot may not move outside the warehouse.
- The warehouse does not "wrap" around.
- As described earlier, the robot may pick up a box that is in an adjacent square.
- The cost to pick up a box is 4, regardless of the direction the box is relative to the robot.
- While holding a box, the robot may not pick up another box.
- The robot may put a box down on an adjacent empty space ('.') or the dropzone ('@') at a cost
  of 2 (regardless of the direction in which the robot puts down the box).
- If a box is placed on the '@' space, it is considered delivered and is removed from the ware-
  house.
- The warehouse will be arranged so that it is always possible for the robot to move to the 
  next box on the todo list without having to rearrange any other boxes.

An illegal move will incur a cost of 100, and the robot will not move (the standard costs for a 
  move will not be additionally incurred). Illegal moves include:
- attempting to move to a nonadjacent, nonexistent, or occupied space
- attempting to pick up a nonadjacent or nonexistent box
- attempting to pick up a box while holding one already
- attempting to put down a box on a nonadjacent, nonexistent, or occupied space
- attempting to put down a box while not holding one

=== Output Specifications ===

`plan_delivery` should return a LIST of moves that minimizes the total cost of completing
  the task successfully.
Each move should be a string formatted as follows:

'move {i} {j}', where '{i}' is replaced by the row-coordinate of the space the robot moves
  to and '{j}' is replaced by the column-coordinate of the space the robot moves to

'lift {x}', where '{x}' is replaced by the alphanumeric character of the box being picked up

'down {i} {j}', where '{i}' is replaced by the row-coordinate of the space the robot puts 
  the box, and '{j}' is replaced by the column-coordinate of the space the robot puts the box

For example, for the values of `warehouse` and `todo` given previously (reproduced below):
  warehouse = ['1#2',
               '.#.',
               '..@']
  todo = ['1','2']
`plan_delivery` might return the following:
  ['move 2 1',
   'move 1 0',
   'lift 1',
   'move 2 1',
   'down 2 2',
   'move 1 2',
   'lift 2',
   'down 2 2']

=== Grading ===

- Your planner will be graded against a set of test cases, each equally weighted.
- If your planner returns a list of moves of total cost that is K times the minimum cost of 
  successfully completing the task, you will receive 1/K of the credit for that test case.
- Otherwise, you will receive no credit for that test case. This could happen for one of several 
  reasons including (but not necessarily limited to):
  - plan_delivery's moves do not deliver the boxes in the correct order.
  - plan_delivery's output is not a list of strings in the prescribed format.
  - plan_delivery does not return an output within the prescribed time limit.
  - Your code raises an exception.

=== Additional Info ===

- You may add additional classes and functions as needed provided they are all in the file `partA.py`.
- Upload partA.py to Project 2 on T-Square in the Assignments section. Do not put it into an 
  archive with other files.
- Your partA.py file must not execute any code when imported.
- Ask any questions about the directions or specifications on Piazza.
'''

import math

class DeliveryPlanner:

    def __init__(self, warehouse, todo):
        self.warehouse = warehouse
        self.todo = todo

    def plan_delivery(self):

        
        sideway_cost = 2
        diagonal_cost = 3
        delta = [[-1, 0 ], # go up
                 [ 0, -1], # go left
                 [ 1, 0 ], # go down
                 [ 0, 1 ], # go right
                 [-1, 1 ], # go top right
                 [-1, -1], # go top left
                 [ 1, 1 ], # go down right
                 [ 1, -1], # go down left
                 ]
        
        #print("Grid World")
        
        #for i in range(len(self.warehouse[0])):
        #    print(self.warehouse[i])

        moves = []
        
        ## Helper Functions
        def compute_heu(grid,goal,delta,sideway_cost,diagonal_cost):
            # ----------------------------------------
            # insert code below
            # ----------------------------------------
            def inGrid(grid, x, y):
                if x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid):
                    return True
                else:
                    return False
            
            value = [[9999 for x in range(len(grid[0]))] for y in range(len(grid))]
            
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
                        if (grid[targetY][targetX] == '.' or grid[targetY][targetX] == '@')  and value[targetY][targetX] == 9999 and i < 4:
                            openList.append([1*(currentCell[0]+ sideway_cost), targetY, targetX])
                            value[targetY][targetX] = 1*(currentCell[0] + sideway_cost)
                        elif (grid[targetY][targetX] == '.' or grid[targetY][targetX] == '@') and value[targetY][targetX] == 9999 and i>=4:
                            openList.append([1*(currentCell[0]+ diagonal_cost), targetY, targetX])
                            value[targetY][targetX] = 1*(currentCell[0] + diagonal_cost)
            return value
        
        def search(grid, init , goal, sideway_cost, diagonal_cost, heuristic, moves):


            closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
            closed[init[0]][init[1]] = 1

            #print(" ")
            #print("closed array in the beginning")
            #for i in range(len(closed[0])):
            #    print(closed[i])
            
            expand = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]

            #print(" ")
            #print("expand array in the beginning")
            #for i in range(len(expand[0])):
            #    print(expand[i])
            #action = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]

            x = init[0]
            y = init[1]
            g = 0
            f = g + heuristic[x][y]

            open_cells = [[f, g, y, x]]
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
                    y = next_cell[2]
                    x = next_cell[3]
                    g = next_cell[1]
                    f = next_cell[0]
                    expand[x][y] = count
                    if(count>0):
                        mv = 'move ' + str(x) +' '+ str(y)
                        moves.append(mv)
                    

                    #print("")
                    #print("expand")
                    #for i in range(len(expand[0])):
                    #    print(expand[i])
                    count += 1
                    
                    if distance_between([x,y],[goal[0],goal[1]]) == 1 or distance_between([x,y],[goal[0],goal[1]]) == math.sqrt(2):
                        found = True
                        return moves
                    else:
                        for i in range(len(delta)):
                            x2 = x + delta[i][0]
                            y2 = y + delta[i][1]
                            if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                                if closed[x2][y2] == 0 and (grid[x2][y2] == '.' or grid[x2][y2] == '@') and i < 4:
                                    g2 =  sideway_cost
                                    f2 = g2 + heuristic[x2][y2]
                                    open_cells.append([f2, g2, y2, x2])
                                    #print("")
                                    #print("after appending open_cells")
                                    #print(open_cells)
                                    closed[x2][y2] = 1
                                elif closed[x2][y2] == 0 and (grid[x2][y2] == '.' or grid[x2][y2] == '@') :
                                    g2 =  diagonal_cost
                                    f2 = g2 + heuristic[x2][y2]
                                    open_cells.append([f2, g2, y2, x2])
                                    #print("")
                                    #print("after appending open_cells")
                                    #print(open_cells)
                                    closed[x2][y2] = 1

            return moves
        
        def distance_between(a,b):
            i,j = a
            p,q = b
            dist = math.sqrt((i-p)**2 + (j-q)**2)
            return dist
        
        ## Plan path to adjacent cell to first package
        ## Identify Position of the first package
        for to in range(len(self.todo)):

            pkg = self.todo[to]

            #print(" ")
            #print("First package:",pkg)
            
            for i in range(len(self.warehouse)):
                for j in range(len(self.warehouse[0])):
                    if(self.warehouse[i][j] == pkg):
                        pkg_pos = [i,j]
                        #print(" ")
                        #print("pkg_pos:",pkg_pos)
                    if(self.warehouse[i][j] == '@'):
                        drop_zone = [i,j]
                        #print(" ")
                        #print("rob_zone:",rob_zone)

            #rel_x = rob_zone[0] - pkg_pos[0]
            #rel_y = rob_zone[1] - pkg_pos[1]
            #print('relative position i:',rel_x,'j:',rel_y)
            
            
            
            ## Build heuristic function based on distance to the package
            heu = compute_heu(self.warehouse, pkg_pos, delta, sideway_cost, diagonal_cost) 

            #print(" ")
            #print("Heuristic Grid")
            #for i in range(len(heu[0])):
            #    print(heu[i])


            if(to == 0):
                final_pos = drop_zone
            
            moves = search(self.warehouse, final_pos, pkg_pos, sideway_cost, diagonal_cost, heu, moves)

            #print(" ")
            #print("Way found")
            #print(moves)
                    
            ## Pickup the package
            moves.append('lift ' + (self.todo[to]))
            #print("")
            #print("moves")
            #print(moves)
            self.warehouse[pkg_pos[0]] = self.warehouse[pkg_pos[0]].replace(self.todo[to],'.')
            ## Plan path to cell adjacent to dropzone
            for i in range(len(moves)):
                    mov = moves[-(i+1)].split()
                    if(mov[0] == 'move'):
                            final_pos = int(mov[1]),int(mov[2])
                            break

            
            heu = compute_heu(self.warehouse, drop_zone, delta, sideway_cost, diagonal_cost)
            
            moves = search(self.warehouse, final_pos, drop_zone, sideway_cost, diagonal_cost, heu, moves)
            #print(" ")
            #print("Way found")
            #print(moves)
                    
            ## Drop the Package
            moves.append('down ' + str(drop_zone[0])+' '+ str(drop_zone[1]))
            for i in range(len(moves)):
                    mov = moves[-(i+1)].split()
                    if(mov[0] == 'move'):
                            final_pos = int(mov[1]),int(mov[2])
                            break
            #print("")
            #print("moves")
            #print(moves)
            ## Repeat for all the packages.
        

        return moves
