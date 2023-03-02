import random as rnd
import queue

# works fine but since there is no book- keeping there is a possibility of going to the previous state even though it was once visited

# and there can be some initial states from where we can never get a solution

# hence, it is required that we give a specific input 

def random_index(m: int):
  x = rnd.randrange(0,m)
  y = rnd.randrange(0,m)
  return (x,y)

def absolute_value(x: int):
  return x if x>=0 else -x

# for different heuristics we have to change the __lt__ function of the class Grid state

class Grid_State:
  def __init__(self,grid: list) -> None:

    self.grid = grid
    self.parent = None
    manhattan_distance_heuristic = 0
    m = len(grid)
    self.length_of_grid = m
    num = 1
    # goal_grid = [
    #   list([0 for _ in range(m)]) for _ in range(m)
    # ]
    # for i in range(m):
    #   for j in range(m):
    #     if (i,j) != (m-1,m-1):
    #       goal_grid[i][j] = num
    #       num += 1
    number_to_index_dictionary = dict()
    num = 1
    for i in range(m):
      for j in range(m):
        if num!=m*m:
          number_to_index_dictionary[num] = (i,j)
          num += 1
    number_to_index_dictionary[0] = (m-1,m-1)
    

    for i in range(m):
      for j in range(m):
        number_in_i_j = grid[i][j]
        actual_pos_of_number = number_to_index_dictionary[number_in_i_j]
        manhattan_distance_heuristic += absolute_value(i-actual_pos_of_number[0]) + absolute_value(j - actual_pos_of_number[1])


    
    self.manhattan_distance_heuristic = manhattan_distance_heuristic
    del number_to_index_dictionary
    self.children_state_of_this_state = list()
    self.number_of_misplaced_blocks = self.compute_number_of_mispaced_tiles()
    self.manhattan_distance_heuristic_of_zero = self.compute_manhattan_distance_of_zero()

  # def compute_manhattan_distance_heuristic(self):

  def __lt__(self,other):
    # return self.manhattan_distance_heuristic < other.manhattan_distance_heuristic
    return self.number_of_misplaced_blocks < other.number_of_misplaced_blocks
    # return self.manhattan_distance_heuristic_of_zero < other.manhattan_distance_heuristic_of_zero

  def compute_number_of_mispaced_tiles(self):
    grid = self.grid
    count = 0
    m = self.length_of_grid
    number = 1
    for i in range(m):
      for j in range(m):
        if (i,j) == (m-1,m-1):
          if grid[i][j] != 0:
            count += 1
        else:
          if grid[i][j] != number:
            count += 1
          number += 1
    return count

  def compute_manhattan_distance_of_zero(self):
    grid = self.grid
    x = 0
    y = 0
    m = self.length_of_grid
    for i in range(m):
      for j in range(m):
        if grid[i][j] == 0:
          x = i
          y = i
          # since m-1 will always be greater than or equal to x and y
          return (m-1)-x + (m-1) - y







class Sliding_Block_Grid:
  def __init__(self, m=3) -> None:
    self.sides =m
    self.rows = m
    self.columns = m
    self.pos_zero = [0,0]
    self.grid = [
      list([-1 for _ in range(m)]) for _ in range(m)
    ]
    
    # to create new list in each row

    # number = 0
    # while number < m*m:
    #   i,j = random_index(m)
    #   if self.grid[i][j] == -1:
    #     self.grid[i][j] = number
    #     if number == 0:
    #       self.pos_zero = [i,j]
        
    #     number += 1

    # self.grid = [
    #   list([int(input()) for _ in range(m)]) for _ in range(m)
    # ]

    self.create_solvable_puzzle()

    self.current_grid_state = Grid_State(self.grid)
    # list of states
    # self.solution = list()

  
  def create_solvable_puzzle(self):
    m = self.sides
    grid = [
      list([0 for _ in range(m)]) for _ in range(m)
    ]
    number = 1
    for i in range(m):
      for j in range(m):
        if (i,j) == (m-1,m-1):
          grid[i][j] = 0
        else:
          grid[i][j] = number
          number+=1
    
    # depth = rnd.randrange(10,20)
    # depth = int(input())
    depth = 6
    i = m-1
    j = m-1
    # continue from here
    for _ in range(depth):
      actionList = self.possible_actions_to_create_solvable_maze(i,j,m)
      action = rnd.choices(actionList,k=1)[0]
      if action=='u':
        grid[i][j], grid[i-1][j] = grid[i-1][j], grid[i][j]
        i,j = i-1,j
      elif action=='d':
        grid[i][j], grid[i+1][j] = grid[i+1][j], grid[i][j]
        i,j = i+1,j
      elif action=='l':
        grid[i][j], grid[i][j-1] = grid[i][j-1], grid[i][j]
        i,j = i,j-1
      elif action == 'r':
        grid[i][j], grid[i][j+1] = grid[i][j+1], grid[i][j]
        i,j = i,j+1
      else:
        pass
    self.grid = grid

      

  
  def possible_actions_to_create_solvable_maze(self,i: int, j:int, m:int):
    # neither corner nor edge
    if i not in [0,m-1] and j not in [0,m-1]:
      return ['u','r','d','l']
    # edge
    elif i not in [0,m-1] and j in [0,m-1]:
      if j==0:
        # left edge
        return ['u','r','d']
      else:
        # right edge
        return ['u','d','l']
    elif i in [0,m-1] and j not in [0,m-1]:
      if i==0:
        # top edge
        return ['r','d','l']
      else:
        # bottom edge
        return ['u','r','l']
    # corners
    else:
      if (i,j)==(0,0):
        # top left
        return ['r','d']
      elif (i,j)==(0,m-1):
        # top right
        return ['d','l']
      elif (i,j)==(m-1,m-1):
        # bottom right
        return ['u','l']
      else:
        # bottom left
        return ['u','r']

  


  def print_current_state_of_grid(self):
    print()
    for i in range(self.sides):
      for j in range(self.sides):
        print(self.grid[i][j],end=' ')
      print()
    # print(f'position of zero is {self.pos_zero}')
    print()
  
  def is_goal_state(self,grid: list):
    number = 1
    m = self.sides
    for i in range(m):
      for j in range(m):
        if (i,j) != (m-1,m-1) and grid[i][j] == number:
          number += 1
        elif (i,j) == (m-1,m-1):
          if grid[i][j] != 0:
            return False
        else:
          return False
    return True



class Agent:
  def __init__(self,puzzle_grid: Sliding_Block_Grid) -> None:

    self.in_puzzle = puzzle_grid
    self.in_grid = puzzle.grid.copy()
    self.length_of_puzzle = puzzle_grid.sides
    self.pos_agent = puzzle_grid.pos_zero
    # need not write list(puzzle_grid.pos_zero) because whenever pos_zero updates, we need the agent's position also to update
    # since list is call by reference
    self.grid_state = Grid_State(puzzle_grid.grid.copy())
    # grid state is initialized with a copy of the list
    # so any modification in this list will not affect in the original list
    self.solution_list = list()
    self.astar_explore_count_manhattan_distance = 0
    self.astar_explore_count_number_of_misplaced_blocks = 0
    self.astar_explore_count_manhattan_distance_of_zero = 0
    

  def possible_actions(self):
    m = self.length_of_puzzle
    i = self.pos_agent[0]
    j = self.pos_agent[1]
    # neither corner nor edge
    if i not in [0,m-1] and j not in [0,m-1]:
      return ['u','r','d','l']
    # edge but not corner
    elif i in [0,m-1] and j not in [0,m-1]:
      if i==0:
        # top edge  
        return ['r','d','l']
      else:
        # bottom edge
        return ['r','l','u']
    elif i not in [0,m-1] and j in [0,m-1]:
      if j==0:
        # left edge
        return ['u','r','d']
      else:
        # right edge
        return ['u','d','l']
    # corner
    else:
      if (i,j) == (0,0):
        # top left
        return ['r','d']
      if (i,j) == (0,m-1):
        # top right
        return ['d','l']
      if (i,j) == (m-1,m-1):
        # bottom right
        return ['u','l']
      else:
        # bottom left
        return ['u','r']

  def possible_actions_from_state(self,grid_state: Grid_State):
    m = self.length_of_puzzle
    pos_agent = self.find_pos_zero(grid_state)

    i = pos_agent[0]
    j = pos_agent[1]
    # neither corner nor edge
    if i not in [0,m-1] and j not in [0,m-1]:
      return ['u','r','d','l']
    # edge but not corner
    elif i in [0,m-1] and j not in [0,m-1]:
      if i==0:
        # top edge  
        return ['r','d','l']
      else:
        # bottom edge
        return ['r','l','u']
    elif i not in [0,m-1] and j in [0,m-1]:
      if j==0:
        # left edge
        return ['u','r','d']
      else:
        # right edge
        return ['u','d','l']
    # corner
    else:
      if (i,j) == (0,0):
        # top left
        return ['r','d']
      if (i,j) == (0,m-1):
        # top right
        return ['d','l']
      if (i,j) == (m-1,m-1):
        # bottom right
        return ['u','l']
      else:
        # bottom left
        return ['u','r']

  def is_goal_state(self,grid_state: Grid_State):
    number = 1
    m = self.length_of_puzzle
    grid = grid_state.grid
    for i in range(m):
      for j in range(m):
        if (i,j) != (m-1,m-1) and grid[i][j] == number:
          number += 1
        elif (i,j) == (m-1,m-1):
          if grid[i][j] != 0:
            return False
        else:
          return False
    return True

  def create_copy(self,puzzle_grid: list):
    copy = [None for _ in range(self.length_of_puzzle)]
    for i in range(self.length_of_puzzle):
      copy[i] = list(puzzle_grid[i])
    return copy
  
  
  
  def find_pos_zero(self,grid_state: Grid_State):
    grid = grid_state.grid
    for i in range(self.length_of_puzzle):
      for j in range(self.length_of_puzzle):
        if grid[i][j] == 0:
          return (i,j)

  def child_generator(self) -> Grid_State:
    current_state_of_grid = self.in_puzzle.grid
    copy_of_current_state_of_grid = self.create_copy(current_state_of_grid)
    possible_actions = self.possible_actions()
    num_possible_actions = len(possible_actions)
    children_list = [
      self.create_copy(copy_of_current_state_of_grid) for _ in range(num_possible_actions)
    ]
    for i in range(num_possible_actions):
      self.do_action(children_list[i],possible_actions[i])
    children_states = [
      Grid_State(child_grid) for child_grid in children_list
    ]
    return children_states

  def child_generator_from_state(self, grid_state: Grid_State):
    grid = list(grid_state.grid)
    possible_actions = self.possible_actions_from_state(grid_state)
    num_possible_actions = len(possible_actions)
    children_list = [
      self.create_copy(grid) for _ in range(num_possible_actions)
    ]
    children_states = [
      Grid_State(child_list) for child_list in children_list
    ]
    for i in range(num_possible_actions):
      self.do_action_from_state(children_states[i],possible_actions[i])
    return children_states

  def do_action_from_state(self,grid_state: Grid_State, action: str):
    pos_agent = self.find_pos_zero(grid_state)
    i = pos_agent[0]
    j = pos_agent[1]
    grid = grid_state.grid
    if action == 'u':
      grid[i][j], grid[i-1][j] = grid[i-1][j], grid[i][j]
    elif action == 'r':
      grid[i][j], grid[i][j+1] = grid[i][j+1], grid[i][j]
    elif action == 'd':
      grid[i][j], grid[i+1][j] = grid[i+1][j], grid[i][j]
    elif action == 'l':
      grid[i][j], grid[i][j-1] = grid[i][j-1], grid[i][j]
    else:
      pass

  def do_action(self,grid: list, action: str):
    i = self.pos_agent[0]
    j = self.pos_agent[1]
    if action == 'u':
      grid[i][j], grid[i-1][j] = grid[i-1][j], grid[i][j]
    elif action == 'r':
      grid[i][j], grid[i][j+1] = grid[i][j+1], grid[i][j]
    elif action == 'd':
      grid[i][j], grid[i+1][j] = grid[i+1][j], grid[i][j]
    elif action == 'l':
      grid[i][j], grid[i][j-1] = grid[i][j-1], grid[i][j]
    else:
      pass

  def astar_search_using_manhattan(self,print_route = True):
    self.astar_explore_count_manhattan_distance = 0
    initial_state = self.grid_state
    # create a queue
    q = queue.PriorityQueue()
    # tuple is priority number, data
    tuple_to_be_added = (initial_state.manhattan_distance_heuristic,initial_state)
    q.put(tuple_to_be_added)

    if self.is_goal_state(initial_state) or initial_state.manhattan_distance_heuristic == 0:
      if print_route:
        print('Solution found')
        self.print_solution(initial_state)
      return


    while not q.qsize == 0:
      self.astar_explore_count_manhattan_distance += 1
      u_state = q.get()[1]
      
      u_state: Grid_State
      children_states = self.child_generator_from_state(u_state)
      for child_state in children_states:
        child_state: Grid_State
        child_state.parent = u_state
        if self.is_goal_state(child_state) or child_state.manhattan_distance_heuristic == 0:
          if print_route:
            print('Solution found')
            self.print_solution(child_state)
          return
        tuple_to_be_added_to_priority_queue = (child_state.manhattan_distance_heuristic,child_state)
        # print('not yet found')
        q.put(tuple_to_be_added_to_priority_queue)

  def astar_search_using_number_of_misplaced_blocks(self,print_route = True):
    self.astar_explore_count_number_of_misplaced_blocks = 0
    initial_state = self.grid_state
    # create a queue
    q = queue.PriorityQueue()
    # tuple is priority number, data
    tuple_to_be_added = (initial_state.number_of_misplaced_blocks,initial_state)
    q.put(tuple_to_be_added)

    if self.is_goal_state(initial_state) or initial_state.number_of_misplaced_blocks == 0:
      if print_route:
        print('Solution found')
        self.print_solution(initial_state)
      return


    while not q.qsize == 0:
      self.astar_explore_count_number_of_misplaced_blocks += 1
      u_state = q.get()[1]
      
      u_state: Grid_State
      children_states = self.child_generator_from_state(u_state)
      for child_state in children_states:
        child_state: Grid_State
        child_state.parent = u_state
        if self.is_goal_state(child_state) or child_state.number_of_misplaced_blocks == 0:
          if print_route:
            print('Solution found')
            self.print_solution(child_state)
          return
        tuple_to_be_added_to_priority_queue = (child_state.number_of_misplaced_blocks,child_state)
        # print('not yet found')
        q.put(tuple_to_be_added_to_priority_queue)

  

  def astar_search_using_manhattan_distance_of_zero(self,print_route = True):
    self.astar_explore_count_manhattan_distance_of_zero = 0
    initial_state = self.grid_state
    # create a queue
    q = queue.PriorityQueue()
    # tuple is priority number, data
    tuple_to_be_added = (initial_state.manhattan_distance_heuristic_of_zero,initial_state)
    q.put(tuple_to_be_added)

    if self.is_goal_state(initial_state):
      if print_route:
        print('Solution found')
        self.print_solution(initial_state)
      return


    while not q.qsize == 0:
      self.astar_explore_count_number_of_misplaced_blocks += 1
      u_state = q.get()[1]
      
      u_state: Grid_State
      children_states = self.child_generator_from_state(u_state)
      for child_state in children_states:
        child_state: Grid_State
        child_state.parent = u_state
        if self.is_goal_state(child_state):
          if print_route:
            print('Solution found')
            self.print_solution(child_state)
          return
        tuple_to_be_added_to_priority_queue = (child_state.manhattan_distance_heuristic_of_zero,child_state)
        # print('not yet found')
        q.put(tuple_to_be_added_to_priority_queue)




  def print_grid(self,grid_state: Grid_State):
    print()
    grid = grid_state.grid
    for i in range(self.length_of_puzzle):
      for j in range(self.length_of_puzzle):
        print(grid[i][j],end=' ')
      print()
    print()

  def print_solution(self,state_of_grid: Grid_State):
    if state_of_grid == None:
      return
    self.print_solution(state_of_grid.parent)
    self.print_grid(state_of_grid)






    



  


puzzle = Sliding_Block_Grid(3)
puzzle.print_current_state_of_grid()
agent = Agent(puzzle_grid=puzzle)
# agent.astar_search_using_manhattan()
agent.astar_search_using_number_of_misplaced_blocks()
# agent.astar_search_using_manhattan_distance_of_zero()


explored = 0
for _ in range(100):
  puzzle_new = Sliding_Block_Grid()
  agent_new = Agent(puzzle_new)
  agent.astar_search_using_number_of_misplaced_blocks(False)
  explored += agent.astar_explore_count_number_of_misplaced_blocks
  del agent_new
  del puzzle_new
print(f'the average number of vertices explored is {explored/100}')


