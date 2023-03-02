import random as rnd
import queue

class Cell:
  def __init__(self,x,y,m) -> None:
    # coordinate is same as index
    self.m = m
    # x coordinate
    self.x = x
    # y coordinate
    self.y = y
    # for printing path, we need parent
    self.parent = None
    # unique cell number for each cell
    self.cell_number = x*m + y
    # isVisited during creating maze
    self.isVisited = False
    # isVisited during searches
    self.isVisited_in_search = False
    # list of adjacent cells
    self.adjCells = []
    # during bfs, to store information of distance
    self.distance = 0
    # manhattan distance heuristic
    self.manhattan_distance_to_last_cell = (m-1-x) + (m-1-y)
    # x and y will always be less than or equal to m-1
    

    # if cell is neither in the corner nor the edge
    if x not in [0,m-1] and y not in [0,m-1]:
      adjCells = [
        (x - 1, y), # up ^
        (x,y+1), # right ->
        (x+1,y), # down v
        (x,y-1) # left
      ]
      self.adjCells = adjCells
    
    elif x not in [0,m-1] and y in [0,m-1]:
      # left and right edge

      if y == 0:
      # left edge
        adjCells = [
          (x - 1, y), # up ^
          (x,y+1), # right ->
          (x+1,y), # down v
          # () # left
        ]
        self.adjCells = adjCells
      else:
        # right edge
        adjCells = [
          (x - 1, y), # up ^
          # (), # right ->
          (x+1,y), # down v
          (x,y-1) # left
        ]
        self.adjCells = adjCells
    
    elif x  in [0,m-1] and y not in [0,m-1]:
      # top and bottom edge

      if x==0:
        # top edge
        adjCells = [
          # (), # up ^
          (x,y+1), # right ->
          (x+1,y), # down v
          (x,y-1) # left
        ]
        self.adjCells = adjCells
      else:
        adjCells = [
          (x - 1, y), # up ^
          (x,y+1), # right ->
          # (), # down v
          (x,y-1) # left
        ]
        self.adjCells = adjCells

    else:
      # corners
      if (x,y) == (0,0):
        # top left corner
        adjCells = [
          # (), # up ^
          (x,y+1), # right ->
          (x+1,y), # down v
          # () # left
        ]
        self.adjCells = adjCells
      elif (x,y) == (0,m-1):
        # top right corner
        adjCells = [
          # (), # up ^
          # (), # right ->
          (x+1,y), # down v
          (x,y-1) # left
        ]
        self.adjCells = adjCells
      elif (x,y) == (m-1,m-1):
        # bottom right corner
        adjCells = [
          (x - 1, y), # up ^
          # (), # right ->
          # (), # down v
          (x,y-1) # left
        ]
        self.adjCells = adjCells
      else:
        # bottom left corner
        adjCells = [
          (x - 1, y), # up ^
          (x,y+1), # right ->
          # (), # down v
          # () # left
        ]
        self.adjCells = adjCells

    adjCell_numbers = [
      adjCell[0]*m + adjCell[1] for adjCell in self.adjCells
    ]
    self.adjCell_numbers = list(adjCell_numbers)
    # the unique cell numbers of adj Cells

    # list of walled neighbours
    self.walled_neighbours = list(self.adjCell_numbers)
    # list of non walled neighbours
    self.non_walled_neighbours = [
      x for x in self.adjCell_numbers if x not in self.walled_neighbours
    ]

  def generate_children_of_cell(self):
    # returns all cells which are adjacent to the current cell, whether walled or non-walled
    return self.adjCell_numbers

  def generate_non_walled_neighbours(self):
    # returns list of non-walled neighbours, the list contains the unique cell numbers
    return self.non_walled_neighbours

  def manhattan_distance_heuristic(self) -> int:
    # returns manhattan distance heuristic
    return self.manhattan_distance_to_last_cell

  def print_current_cell(self):
    # utility function to print the attributes of the current cell
    print()
    print(f'the cell is {(self.x,self.y)}')
    print(f'the cell number is {self.cell_number}')
    print(f'the adj Cells are {self.adjCells}')
    print(f'the adjCell numbers are {self.adjCell_numbers}')
    print(f'the walled neighbours are {self.walled_neighbours}')
    print(f'the non-walled neighbours are {self.non_walled_neighbours}')
    print()
  
  def print_adjacency_list(self):
    # prints the list of non-walled neighbours of the current cell
    print()
    x = self.non_walled_neighbours
    y = [
      (int(cell_number/self.m),cell_number%self.m)
      for cell_number in x
    ]
    print(f'Node {(self.x,self.y)}: ', end=' ')
    for coord in y:
      print(coord,end=' ')
    print()
    print()

  # the below function is for the purpose of priority queue, when using priority queue, python internally compares 2 instances of cell object, when priority number is same 
  def __lt__(self,other):
    return self.manhattan_distance_to_last_cell < other.manhattan_distance_to_last_cell
    # return True


class Maze:
  def __init__(self,m) -> None:
    # maze side length
    self.sides = m
    # list of 'Cell' Objects
    self.cells = [Cell(i,j,m) for i in range(m) for j in range(m)]
    # creating an empty dictionary to store all the cells with key as the the unique cell number
    # the reason for using dictionary is to access the elements fast
    self.cell_dictionary = dict()
    for cell in self.cells:
      # the key of each cell is of the form 'cell_{cell number}'
      self.cell_dictionary[f'cell_{cell.cell_number}'] = cell
    # self.created_maze = self.generate_maze()
    # we call generate_maze() function to generate a random maze
    self.generate_maze()
    # maze_img is a list of list which is used to print the grid of maze
    self.maze_img = [
      list(['' for _ in range(2*m + 1)]) for _ in range(2*m + 1)
    ]
    # calling create_maze_img() function to create the maze image
    self.create_maze_img()
    # since list is mutable, we have to create new list in every row

  def generate_maze(self):
    # we are generating maze using randomized depth first search
    self.dfs_create_maze(self.cell_dictionary['cell_0'])

  def child_generator(self,cell: Cell):
    # returns the adjacent cells of the cell, the list will contain the cell numbers
    return cell.generate_children_of_cell()

  def dfs_create_maze(self,cell: Cell):
    # create maze function

    # length of maze
    m = self.sides

    # adj cells of the current cell
    adj_cell_number_list = list(cell.generate_children_of_cell())
    # adj_cells = cell.generate_children_of_cell().copy()

    # we are shuffling it in order to simulate randomized picking of cells
    rnd.shuffle(adj_cell_number_list)

    # isVisited in creating maze is set to True
    cell.isVisited = True

    # for each cell in the adj cells
    for cell_to_be_considered in adj_cell_number_list:
      cell_to_be_considered: int

      # using a try except block in order to catch any possible errors
      try:
        cellCheck = self.cell_dictionary[f'cell_{cell_to_be_considered}']
      except:
        print(f'the key {cell_to_be_considered} not found')
      cellCheck: Cell
      if cellCheck.isVisited == False:
        # if cell is not visited
        # first remove wall between this cell and the picked cell
        try:
          cell.walled_neighbours.remove(cellCheck.cell_number)
        except:
          print(f'cell {cellCheck.cell_number} not found in {cell.cell_number}\'s{cell.walled_neighbours}')
        cell.non_walled_neighbours.append(cellCheck.cell_number)
        # now remove wall between picked cell and this cell
        try:
          cellCheck.walled_neighbours.remove(cell.cell_number)
        except:
          print(f'cell {cell.cell_number} not found in {cellCheck.cell_number}\'s{cell.walled_neighbours}')
        cellCheck.non_walled_neighbours.append(cell.cell_number)

        # then call dfs_create_maze with the non visited cell
        self.dfs_create_maze(cellCheck)
    del adj_cell_number_list
    # in order to save memory


    


  def print_cells_of_maze(self):
    # utility function to print the cell number of cells of maze in the dictionary with their keys
    for key,value in self.cell_dictionary.items():
      value: Cell
      print(key,value.cell_number)
      

  def create_maze_img(self):
    # in order to create the maze image
    m = self.sides
    for i in range(2*self.sides + 1):
      if i%2 == 0:
        for j in range(2*self.sides + 1):
          
          if i==0 or i==2*self.sides:
            # borders
            if j%2 == 0:
              self.maze_img[i][j] = '+'
            else:
              self.maze_img[i][j] = '---'
          # now we have to check if the neighbours are walled
          else:
            

            if j%2 == 0:
              self.maze_img[i][j] = '+'
            else:
              # we can check the list of non walled neighbours
            

              # this will also work if the cell is near the wall because the below cell will not exist in the list of non_walled_neighbours, hence it will be walled
              (x,y) = (int((i-1)/2),int((j-1)/2))
              cNum = x*m + y
              # to check if the below cell is walled in order to decide whether to put wall in the image or not
              is_below_cell_walled = True
              try:
                current_cell = self.cell_dictionary[f'cell_{cNum}']
              except:
                print(f'the key {cNum} not found ')
              current_cell: Cell
              if cNum+m in current_cell.non_walled_neighbours:
                # if below cell is present in non walled neighbours, we update is_below_cell_walled to False
                is_below_cell_walled = False

              
              if is_below_cell_walled:
                self.maze_img[i][j] = '---'
              else:
                self.maze_img[i][j] = '   '


      else:
        for j in range(2*self.sides + 1):
          (x,y) = (int((i-1)/2),int((j-1)/2))
          if j==0 or j==2*self.sides:
            # for left and right boundaries
            self.maze_img[i][j] = '|'
          # if j%2 == 0:
          #   self.maze_img[i][j] = '|'
          else:
            
            if j%2 == 1:
              self.maze_img[i][j] = ''
            else:
              (x,y) = (int((i-1)/2),int((j-1)/2))
              cNum = x*m + y
              # to check if the right cell is walled in order to decide whether to put wall in the image or not
              is_right_cell_walled = True
              # current_cell = self.cell_dictionary[f'cell_{cNum}']
              try:
                current_cell = self.cell_dictionary[f'cell_{cNum}']
              except:
                print(f'the key {cNum} not found ')
              current_cell: Cell
              if cNum+1 in current_cell.non_walled_neighbours:
                # if right cell is in non-walled neighbours, we update is_right_cell_walled to False
                is_right_cell_walled = False
              
              # self.maze_img[i][j] = '|'

              if is_right_cell_walled:
                self.maze_img[i][j] = '|'
              else:
                self.maze_img[i][j] = ''

            


  def print_maze(self):
    # utility function to print the adjacency list of maze cells and image of maze
    for key, cell in self.cell_dictionary.items():
      cell: Cell
      # cell.print_current_cell()
      cell.print_adjacency_list()
    for i in range(2*self.sides + 1):
      if i%2 == 0:
        for j in range(2 * self.sides + 1):
          if j%2 == 0:
            # print('+',end='')
            print(self.maze_img[i][j],end='')
          else:
            # print('---',end='')
            print(self.maze_img[i][j],end='')
        print()
      else:
        for j in range(2 * self.sides + 1):
          # if j==0 or j==2*self.sides:
          if j%2 == 0:
            # print('|',end=' ')
            print(self.maze_img[i][j],end=' '  if self.maze_img[i][j] == '|' else '  ')
          else:
            # print('',end='  ')
            print(self.maze_img[i][j],end='  ')
        print()



# 1b

class Agent:
  def __init__(self,maze: Maze) -> None:
    # which maze is the agent present in
    self.in_maze = maze
    # initial location of the agent is [0,0]
    self.initial_loc = [0,0]
    # attribute to count the number of dfs_explore
    self.dfs_explore_count = 0
    # attribute to count the number of bfs_explore
    self.bfs_explore_count = 0
    # attribute to count the number of astar_explore
    self.astar_explore_count = 0

  def is_goal(self,cellNum):
    # if the agent is in the last cell, then goal state has reached
    m = self.in_maze.sides
    if cellNum == m*m - 1:
      return True
    return False


  def dfs_search(self,print_path = True):
    # initializing dfs_explore count to zero
    self.dfs_explore_count = 0
    maze = self.in_maze
    cell_dictionary = maze.cell_dictionary
    # initializing the parent of each cell to None and is Visited in search of each cell to False
    for i in range(maze.sides * maze.sides):
      cell = cell_dictionary[f'cell_{i}']
      cell: Cell
      cell.parent = None
      cell.isVisited_in_search = False
    # for _,cell in cell_dictionary.items():
    for i in range(maze.sides * maze.sides):
      cell = cell_dictionary[f'cell_{i}']
      cell: Cell
      isPathFound = False
      # isPathFound is to check if path has been found 
      # if path is found, then we can stop the dfs there
      if cell.isVisited_in_search == False:
        # print(f'Going to cell {cell.cell_number}')
        isPathFound = self.dfs_explore(cell)

        # self.dfs_explore(cell)
      if isPathFound == True:
        if print_path:
          print('Path found from initial cell to final cell using DFS')
          # self.print_path(cell_dictionary[f'cell_{maze.sides * maze.sides - 1}'])
          self.print_path(cell_dictionary[f'cell_{maze.sides * maze.sides - 1}'])
          print()
          print(f'the number of cells explored are {self.dfs_explore_count}')
        # break
        return
    # self.print_path(cell_dictionary[f'cell_{maze.sides * maze.sides - 1}'])
    
  def dfs_explore(self,current_cell: Cell):
    # print(f'coming to cell {current_cell.cell_number}')
    
    # dfs explore count increases whenever it comes to this function call
    self.dfs_explore_count += 1

    # updating is visited in search to True
    current_cell.isVisited_in_search = True


    maze = self.in_maze
    cell_dictionary = maze.cell_dictionary

    # taking the non-walled neighbours because agent can only go to those cells which are non-walled with the current cell
    adj_non_walled_neighbours = current_cell.non_walled_neighbours

    # initializing isPath_found to False
    isPath_found = False

    for adjCellNum in adj_non_walled_neighbours:
      try:
        adjCell = cell_dictionary[f'cell_{adjCellNum}']
      except:
        print(f'the key {adjCellNum} is not found')
      adjCell: Cell
      if adjCell.isVisited_in_search == False:
        # if adj non-walled neighbour is unvisited we set the parent of that cell to current cell
        adjCell.parent = current_cell

        if self.is_goal(adjCellNum):
          # if that cell is a goal state

          # print(f'Going to cell {adjCell.cell_number}')
          # self.dfs_explore_count += 1
          # print('Path found')
          # print('Path found from initial cell to final cell using DFS')
          # self.print_path(adjCell)
          # print()

          # if that cell is a goal state, we return True
          return True
        else:
          # print(f'Going to cell {adjCell.cell_number}')
          
          # we set the isPath to the value coming from the next function call
          isPath_found = self.dfs_explore(adjCell)
          if isPath_found:
            return isPath_found
          # print(f'Returned to {current_cell.cell_number}')
          # return isPath_found
          continue
    # print(f'Returning from cell {current_cell.cell_number}')

    # we have to return isPath found from each dfs_explore calls
    return isPath_found
    
  def bfs_search(self,print_path = True):
    # print('in bfs search')
    # initializing explore count to zero
    self.bfs_explore_count = 0
    maze = self.in_maze
    cell_dictionary = maze.cell_dictionary

    # initializing each cell's parent to None and distance to -1 and isVisited in search to False
    for i in range(maze.sides * maze.sides):
      cell = cell_dictionary[f'cell_{i}']
      cell: Cell
      cell.parent = None
      cell.isVisited_in_search = False
      cell.distance = -1

    # using a queue for dfs
    q = queue.Queue()

    # source cell is the cell from where we start bfs, in this case initial cell
    source_cell = cell_dictionary[f'cell_{0}']
    source_cell: Cell
    # q.put(source_cell,timeout=0.0045)
    q.put(source_cell)
    # q.put_nowait(source_cell)
    source_cell.distance = 0
    # Use qsize() == 0 as a direct substitute, but be aware that either approach risks a race condition where a queue can grow before the result of empty() or qsize() can be used.
    # the above was a warning which came when trying to use while q.empty()
    while not q.qsize() == 0:
      # print('executing while loop')
      # u_cell = q.get(timeout=0.0045)
      # u_cell = q.get_nowait()

      # to verify its not a priority queue

      # print('printing queue')
      # for x in q.queue:
      #   x: Cell
      #   print(x.manhattan_distance_to_last_cell,end=' ')
      # print()

      # dequeueing the first cell in the queue
      u_cell = q.get()
      # a cell gets explored only when it comes to while loop
      self.bfs_explore_count += 1
      u_cell: Cell

      # updating the isvisited in search to True
      u_cell.isVisited_in_search = True

      # checking the non-walled neighbours of the current cell
      adj_cell_numbers = u_cell.generate_non_walled_neighbours()

      # for each non walled cell
      for cellNum in adj_cell_numbers:
        # cell_to_check = cell_dictionary[f'cell_{cellNum}']
        try:
          cell_to_check = cell_dictionary[f'cell_{cellNum}']
        except:
          print(f'the key {cellNum} not found')
        cell_to_check: Cell
        if cell_to_check.distance == -1:
          # if distance is -1, it means, it has not been visited yet
          cell_to_check.distance = u_cell.distance + 1
          q.put(cell_to_check)
          # enqueuing into the queue

          # q.put(cell_to_check,timeout=0.0045)
          # q.put_nowait(cell_to_check)
          cell_to_check.parent = u_cell

          # checking if the cell is a goal state
          if self.is_goal(cellNum):
            if print_path:
              print('Path Found from initial cell to final cell using BFS')
              self.print_path(cell_to_check)
              print()
              print(f'the number of vertices explore is {self.bfs_explore_count}')
            del q
            return
      # return
    # del q
    # return
  

  def astar_search(self,print_path = True):
    # initializing explore count to zero
    self.astar_explore_count = 0
    maze = self.in_maze
    cell_dictionary = maze.cell_dictionary

    # initializing each cell's parent to None and distance to -1 and isVisited in search to False
    for i in range(maze.sides * maze.sides):
      cell = cell_dictionary[f'cell_{i}']
      cell: Cell
      cell.parent = None
      cell.isVisited_in_search = False
      cell.distance = -1
    
    # using a priority queue
    q = queue.PriorityQueue()
    source_cell = cell_dictionary[f'cell_{0}']
    source_cell: Cell
    source_cell.distance = 0
    # g function is initially zero
    g_function = 0

    # entries into the queue are of the form (priority number,data)
    # priority queue is based on f = g + h
    q.put((source_cell.manhattan_distance_heuristic()+g_function,source_cell))
    while not q.qsize() == 0:

      # to verify its a priority queue
      # print('printing queue')
      # for x in q.queue:
      #   print(x[0],end=' ')
      # print()

      u_cell = q.get()[1]
      # print(u_cell)
      self.astar_explore_count += 1
      # only when we come to this while loop will we increment the explore count
      u_cell: Cell
      u_cell.isVisited_in_search = True
      # taking the adj cells which are non walled
      adj_cell_numbers = u_cell.generate_non_walled_neighbours()

      # for each cell in adj non walled neighbours
      for cellNum in adj_cell_numbers:
        try:
          cell_to_check = cell_dictionary[f'cell_{cellNum}']
        except:
          print(f'the key {cellNum} not found')
        cell_to_check: Cell
        if cell_to_check.distance == -1:
          cell_to_check.distance = u_cell.distance + 1
          # g function is the distance
          to_add = ((cell_to_check.manhattan_distance_heuristic() + cell_to_check.distance,cell_to_check))

          q.put(to_add)
          # updating the parent cell
          cell_to_check.parent = u_cell
          if self.is_goal(cellNum):
            # checking if its a goal state
            if print_path:
              print('Path Found from initial cell to final cell using A*')
              self.print_path(cell_to_check)
              print()
              print(f'the number of vertices explored is {self.astar_explore_count}')
            del q
            return


  def print_path(self,cell: Cell):
    # this is the recursive print path function
    if not cell:
      # if cell is None, then return
      return
    # else print path of parent and then print the current cell
    self.print_path(cell.parent)
    print((cell.x,cell.y),end=' ')

  def print_parent(self):
    # utility function to print the parent of each cell
    cell_dictionary = self.in_maze.cell_dictionary
    for _,cell in cell_dictionary.items():
      cell: Cell
      parent = cell.parent
      parent: Cell

      print(cell.cell_number, 'parent is', parent.cell_number if parent else None)


# creating a new maze of side length 3
maze = Maze(3)
# maze.print_cells_of_maze()
maze.print_maze()
# printing the adjacency list of maze cells and the image of maze

search_agent = Agent(maze)
search_agent.dfs_search()
# search_agent.print_parent()
search_agent.bfs_search()
search_agent.astar_search()
# search_agent.print_parent()


# for i in range(3):
#   for j in range(3):
#     x = Cell(i,j,3)
#     x.print_current_cell()

# to see the efficiency of dfs,bfs and astar

bfs_explore = 0
dfs_explore = 0
astar_explore = 0


for i in range(100):
  # maze_new = Maze(30)
  maze_new = Maze(10)
  agent_new = Agent(maze_new)
  agent_new.dfs_search(print_path=False)
  dfs_explore += agent_new.dfs_explore_count
  agent_new.bfs_search(print_path=False)
  bfs_explore += agent_new.bfs_explore_count
  agent_new.astar_search(print_path=False)
  astar_explore += agent_new.astar_explore_count
  del agent_new
  del maze_new

print(f'average number of vertices DFS explored: {dfs_explore/100}')
print(f'average number of vertices BFS explored: {bfs_explore/100}')
print(f'average number of vertices A * explored: {astar_explore/100}')




