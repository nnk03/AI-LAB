import random as rnd
import queue




class Cell:
  def __init__(self,position_x,position_y,rows,columns) -> None:
    self.x = position_x
    self.y = position_y
    self.coordinates = (position_x,position_y)
    adjCells_coordinates = []
    self.isVisited = False
    

    # stored in the form [top ^, right ->, bottom v, left <-]
    if position_x <= rows-2 and position_x >= 1 and position_y <= columns - 2 and position_y >=1:
      adjCells_coordinates = [
        (position_x,position_y+1), # top ^
        (position_x+1,position_y), # right ->
        (position_x,position_y-1), # bottom v
        (position_x-1,position_y) # left <-
      ]


    elif position_x in [0,rows-1] and position_y not in [0,columns - 1]:
      # left edges or right edges except corners
      if position_x == 0:
        # left edge
        adjCells_coordinates = [
          (position_x,position_y+1), # top ^
          (position_x+1,position_y), # right ->
          (position_x,position_y-1), # bottom v
          tuple() # left <-
        ]
      else:
        # right edge
        adjCells_coordinates = [
          (position_x,position_y+1), # top ^
          tuple(), # right ->
          (position_x,position_y-1), # bottom v
          (position_x-1,position_y) # left <-
        ]


    elif position_y in [0,columns - 1] and position_x not in [0,rows - 1]:
      # top edges or bottom edges except corners
      if position_y == 0:
        # bottom edge
        adjCells_coordinates = [
          (position_x,position_y+1), # top ^
          (position_x+1,position_y), # right ->
          tuple(), # bottom v
          (position_x-1,position_y) # left <-
        ]
      else:
        # top edge
        adjCells_coordinates = [
          tuple(), # top ^
          (position_x+1,position_y), # right ->
          (position_x,position_y-1), # bottom v
          (position_x-1,position_y) # left <-
        ]
    
    else:
      # corners
      if (position_x,position_y) == (0,0):
        # bottom left
        adjCells_coordinates = [
          (position_x,position_y+1), # top ^
          (position_x+1,position_y), # right ->
          tuple(), # bottom v
          tuple() # left <-
        ]
      
      elif (position_x,position_y) == (0,columns - 1):
        # top left
        adjCells_coordinates = [
          tuple(), # top ^
          (position_x+1,position_y), # right ->
          (position_x,position_y-1), # bottom v
          tuple() # left <-
        ]
      elif (position_x,position_y) == (rows - 1,columns - 1):
        # top right
        adjCells_coordinates = [
          tuple(), # top ^
          tuple(), # right ->
          (position_x,position_y-1), # bottom v
          (position_x-1,position_y) # left <-
        ]
      else:
        # bottom right
        adjCells_coordinates = [
          (position_x,position_y+1), # top ^
          tuple(), # right ->
          tuple(), # bottom v
          (position_x-1,position_y) # left <-
        ]

    self.adjCells_coordinates = adjCells_coordinates
    self.adjCells_coord_isWalled = [
      [x[0],x[1],True] for x in adjCells_coordinates if x 
    ]
  
  def child_generator(self):
    return list([
      x for x in self.adjCells_coord_isWalled if x
    ])
    

  def printCurrentCell(self):
    print(f'The current cell is {self.coordinates}')
    print(f'the adjacent cells are {self.adjCells_coordinates}')


# cell = Cell(int(input()),int(input()),3,3)
# cell.printCurrentCell()
# print(cell.adjCells_coord_isWalled)
# print(cell.child_generator())


# class DFS:
#   def __init__(self) -> None:
#     pass

#   def child_generator(self,x,y)


class Maze:
  def __init__(self,m) -> None:
    self.sides = m
    self.cells = [
      Cell(j,m-i-1,m,m) for i in range(m) for j in range(m)
    ]
    self.cells_dictionary = dict()
    index = 1
    for cell in self.cells:
      self.cells_dictionary[f'cell_{cell.y * self.sides + cell.x + 1}'] = cell
      index += 1
    


  def print_cells(self):
    # for cell in self.cells:
    #   cell.printCurrentCell()
    # print(self.cells_dictionary)
    # for key,cell in self.cells_dictionary:
    #   print(key, end=' ')
    #   cell.printCurrentCell()
    for key in list(self.cells_dictionary.keys()):
      print(key,end=' ')
      cell = self.cells_dictionary[key]
      cell: Cell
      cell.printCurrentCell()
  def generate_maze(self):
    self.dfs_generate(cell= self.cells_dictionary['cell_1'])


  def dfs_generate(self,cell: Cell):
    m = self.sides
    adj_cells = cell.child_generator()
    rnd.shuffle(adj_cells)
    cell.isVisited = True
    for adj_cell_coord_is_walled in adj_cells:
      adj_x = adj_cell_coord_is_walled[0]
      # x coordinate
      adj_y = adj_cell_coord_is_walled[1]
      # y coordinate
      # cellCheck = self.cells_dictionary[f'cell_{adj_x + adj_y * self.sides}']
      adj_cell_toBeConsidered = self.cells_dictionary[f'cell_{adj_x + adj_y * self.sides}']
      if adj_cell_toBeConsidered.isVisited == False:
        neighbour_list = cell.adjCells_coord_isWalled
        for i in range(len(neighbour_list)):
          if neighbour_list[i] == [adj_x,adj_y,True]:
            neighbour_list[i] = [adj_x,adj_y,False]
            break
        
        adj_cell_toBeConsidered : Cell
        neighbours = adj_cell_toBeConsidered.adjCells_coord_isWalled
        for i in range(len(neighbours)):
          if neighbours[i] == [cell.x,cell.y,True]:
            neighbours[i] == [cell.x,cell.y,False]
            break
        
          self.dfs_generate(adj_cell_toBeConsidered)
      

  











maze = Maze(3)
# maze.print_cells()
maze.generate_maze()
cells_dictionary = maze.cells_dictionary

for key in list(cells_dictionary.keys()):
  cell = cells_dictionary[key]
  cell: Cell
  print(key, end='     *******     ')
  print(cell.adjCells_coord_isWalled)



# for cell in maze.cells:
#   print(cell.child_generator())







