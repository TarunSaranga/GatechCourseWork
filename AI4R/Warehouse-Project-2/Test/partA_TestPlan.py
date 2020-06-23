import math
isDebug = False
def plan_delivery():

        warehouse = ['#######2',
                     '#......1',
                     '#@......']
        todo = ['1', '2']
                  
        
        #print(len(warehouse[0][0]))
        #warehouse[0]
        #wh = [[ 0 for i in range(len(str(warehouse[0][0])))] for j in range(len(warehouse))]
        
        #for i in range(len(wh[0])):
        #    for j in range(len(wh)):
        #        wh[i][j] = str(warehouse[i][0])[j]
                
        #warehouse = wh
        #warehouse = [['3','#','@'],
        #             ['2','#','.'],
        #             ['1','.','.']]
        #todo = ['1', '2', '3']

        ## Define movement Cost
        sideway_cost = 2
        diagonal_cost = 3
        delta = [[ -1,0 ], # go left
                 [ 0, -1], # go up
                 [ 1, 0 ], # go down
                 [ 0, 1 ], # go right
                 [-1, 1 ], # go top right
                 [-1, -1], # go top left
                 [ 1, 1 ], # go down right
                 [ 1, -1], # go down left
                 ]
        
        print("Grid World")
        
        for i in range(len(warehouse)):
            print(warehouse[i])

        moves = []
        
        ## Helper Functions
        def compute_heu(grid,goal,next_goal,delta,sideway_cost,diagonal_cost):
            # ----------------------------------------
            # insert code below
            # ----------------------------------------
            def inGrid(grid, x, y):
                if x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid):
                    return True
                else:
                    return False
            
            value = [[9999 for x in range(len(grid[0]))] for y in range(len(grid))]
            #dist = [[9999 for x in range(len(grid[0]))] for y in range(len(grid))]
            #dist_added = [[9999 for x in range(len(grid[0]))] for y in range(len(grid))]
            
            value[goal[0]][goal[1]] = 0
            #dist[next_goal[0]][next_goal[1]] = 0
            #dist_added[goal[0]][goal[1]] = 0
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
                            openList.append([1*(currentCell[0] + sideway_cost ), targetY, targetX])
                            value[targetY][targetX] = 1*(currentCell[0] + sideway_cost )
                            #dist[targetY][targetX] = 1*(int(distance_between(next_goal,[targetY,targetX])**3) )
                            #dist_added[targetY][targetX] = value[targetY][targetX] + dist[targetY][targetX]
                        elif (grid[targetY][targetX] == '.' or grid[targetY][targetX] == '@') and value[targetY][targetX] == 9999 and i>=4:
                            openList.append([1*(currentCell[0] + diagonal_cost ), targetY, targetX])
                            value[targetY][targetX] = 1*(currentCell[0] + diagonal_cost )
                            #dist[targetY][targetX] = 1*(int(distance_between(next_goal,[targetY,targetX])**3) )
                            #dist_added[targetY][targetX] = value[targetY][targetX] + dist[targetY][targetX]

##            print('')
##            print("Distance Matrix")
##            for i in range(len(dist)):
##                    print(dist[i])
##
##            print('')
##            print("Distance_added Matrix")
##            for i in range(len(dist_added)):
##                    print(dist_added[i])                                   
                            
            return value
        
        def search(grid, init , goal, sideway_cost, diagonal_cost, heuristic, moves):

            closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
            closed[init[0]][init[1]] = 1

            print(" ")
            print("closed array in the beginning")
            for i in range(len(closed)):
                print(closed[i])
            
            expand = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]

            print(" ")
            print("expand array in the beginning")
            for i in range(len(expand)):
                print(expand[i])
            #action = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]

            x = init[0]
            y = init[1]
            g = 0
            f = g + heuristic[x][y]

            open_cells = [[f, g, y, x]]
            print("")
            print("open_cells:")
            print(open_cells)

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
                    print("")
                    print("open_cell after sorting")
                    print(open_cells)
                    next_cell = open_cells.pop()

                    print("")
                    print("Next_cell")
                    print(next_cell)
                    y = next_cell[2]
                    x = next_cell[3]
                    g = next_cell[1]
                    f = next_cell[0]
                    expand[x][y] = count
                    if(count>0):
                        mv = 'move ' + str(x) + ' ' + str(y)
                        moves.append(mv)
                    

                    print("")
                    print("expand")
                    for i in range(len(expand)):
                        print(expand[i])
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
                                    print("")
                                    print("after appending open_cells")
                                    print(open_cells)
                                    closed[x2][y2] = 1
                                elif closed[x2][y2] == 0 and (grid[x2][y2] == '.' or grid[x2][y2] == '@') :
                                    g2 =  diagonal_cost
                                    f2 = g2 + heuristic[x2][y2]
                                    open_cells.append([f2, g2, y2, x2])
                                    print("")
                                    print("after appending open_cells")
                                    print(open_cells)
                                    closed[x2][y2] = 1

            return moves
        
        def distance_between(a,b):
            i,j = a
            p,q = b
            dist = math.sqrt((i-p)**2 + (j-q)**2)
            return dist
        
        ## Plan path to adjacent cell to first package
        ## Identify Position of the first package
        for to in range(len(todo)):
            pkg = todo[to]
            if(to+1<len(todo)):
                    pkg_1 = todo[to+1]
            else:
                    pkg_1 = pkg

            print(" ")
            print("package:",pkg)
            
            for i in range(len(warehouse)):
                for j in range(len(warehouse[0])):
                    if(warehouse[i][j] == pkg_1):
                        pkg1_pos = [i,j]
                        print(" ")
                        print("pkg1_pos:",pkg1_pos)
                    if(warehouse[i][j] == pkg):
                        pkg_pos = [i,j]
                        print(" ")
                        print("pkg_pos:",pkg_pos)
                    if(warehouse[i][j] == '@'):
                        drop_zone = [i,j]
                        print(" ")
                        print("drop_zone:",drop_zone)

            #rel_x = rob_zone[0] - pkg_pos[0]
            #rel_y = rob_zone[1] - pkg_pos[1]
            #print('relative position i:',rel_x,'j:',rel_y)
            
            
            
            ## Build heuristic function based on distance to the package
##            heu = [[0 for i in range(len(warehouse[0]))] for j in range(len(warehouse))]
##            for i in range(len(warehouse)):
##                print(' ')
##                for j in range(len(warehouse[0])):
##                    heu[i][j] = int(3*distance_between([i,j],pkg_pos))
##                    up = i-1
##                    down = i+1
##                    left = j-1
##                    right = j+1
##                    cost = (up < 0) + (down > len(warehouse)-1) + (left < 0) + (right > len(warehouse[0])-1)
##                    if(left > 0 and warehouse[i][left]=='#'):
##                            cost += 1
##                    elif(right < len(warehouse[0]) and warehouse[i][right]=='#'):
##                            cost += 1
##                                    
##                    print(cost)
##                    if(cost>2):
##                        heu[i][j] += cost
            heu = compute_heu(warehouse, pkg_pos,pkg1_pos, delta, sideway_cost, diagonal_cost)
                            
            
            print(" ")
            print("Heuristic Grid")
            for i in range(len(heu)):
                print(heu[i])

            if(to == 0):
                    final_pos = drop_zone
                    
            print('')
            print('final_pos')
            print(final_pos)
            moves = search(warehouse, final_pos, pkg_pos, sideway_cost, diagonal_cost, heu, moves)

            print(" ")
            print("Way found")
            print(moves)
                    
            ## Pickup the package
            moves.append('lift ' + todo[to])
            print("")
            print("moves")
            print(moves)
            warehouse[pkg_pos[0]] = warehouse[pkg_pos[0]].replace(todo[to],'.')
            ## Plan path to cell adjacent to dropzone
            #if(len(moves)>1):
            #    final_pos = moves[-2][-3:]
            #    i,j = int(final_pos[0]), int(final_pos[2])
            #    final_pos = [i,j]
            #    print("Final Pos")
            #    print(final_pos)
            #else:
            #    print("Final Pos")
            #    print(final_pos)
            for i in range(len(moves)):
                    mov = moves[-(i+1)].split()
                    if(mov[0] == 'move'):
                            final_pos = int(mov[1]),int(mov[2])
                            break

            print("Final Pos")
            print(final_pos)
            
##            heu = [[0 for i in range(len(warehouse[0]))] for j in range(len(warehouse))]
##            for i in range(len(warehouse)):
##                print(' ')
##                for j in range(len(warehouse[0])):
##                    heu[i][j] = int(3*distance_between([i,j],drop_zone))
##                    up = i-1
##                    down = i+1
##                    left = j-1
##                    right = j+1
##                    cost = (up < 0) + (down > len(warehouse)-1) + (left < 0) + (right > len(warehouse[0])-1)
##                    if(left > 0 and warehouse[i][left]=='#'):
##                            cost += 1
##                    elif(right < len(warehouse[0]) and warehouse[i][right]=='#'):
##                            cost += 1
##                                    
##                    print(cost)
##                    if(cost>2):
##                        heu[i][j] += cost
            heu = compute_heu(warehouse, drop_zone,drop_zone, delta, sideway_cost, diagonal_cost)
            
            print(" ")
            print("Heuristic Grid")
            for i in range(len(heu)):
                print(heu[i])
            moves = search(warehouse, final_pos, drop_zone, sideway_cost, diagonal_cost, heu, moves)
            print(" ")
            print("Way found")
            print(moves)
                    
            ## Drop the Package
            moves.append('down ' + str(drop_zone[0])+' '+ str(drop_zone[1]))
            print("")
            print("moves")
            print(moves)

            for i in range(len(moves)):
                    mov = moves[-(i+1)].split()
                    if(mov[0] == 'move'):
                            final_pos = int(mov[1]),int(mov[2])
                            break
            print("Final Pos")
            print(final_pos)
##            final_pos = moves[-2][-3:]
##            if(final_pos[0] != 't'): 
##                    i,j = int(final_pos[0]), int(final_pos[2])
##                    final_pos = [i,j]
##                    print("Final Pos")
##                    print(final_pos)
##            elif(final_pos[0] == 't'):
##                 final_pos = moves[-3][-3:]
##                 i,j = int(final_pos[0]), int(final_pos[2])
##                 final_pos = [i,j]
##                 print("Final Pos")
##                 print(final_pos)
            ## Repeat for all the packages.
        

        return moves

moves = plan_delivery()
