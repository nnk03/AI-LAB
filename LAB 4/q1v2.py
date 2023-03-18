import copy
import random as rnd


class TicTacToe_Grid_State:
  def __init__(self,grid_list: list[list],m = 3) -> None:
    # [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    self.grid_side_length = m
    self.grid_list = copy.deepcopy(grid_list)
    # its a list of list of strings (which is immutable)
    # self.vacant_position_indices = self.find_num_of_vacant_positions()
    self.parent = None
    self.utility = -10


  
  def find_num_of_vacant_positions(self):
    m = self.grid_side_length
    vacant_list = list()
    for i in range(m):
      for j in range(m):
        if self.grid_list[i][j] == ' ':
          vacant_list.append((i,j))
    return list(vacant_list)
  
  def print_current_grid_state(self):
    # print()
    # for row in self.grid_list:
    #   print(row)
    # print()
    side_length = 2*self.grid_side_length - 1
    grid_img =[
      list([' ' for _ in range(side_length)]) for _ in range(side_length)
    ]
    for i in range(side_length):
      if i%2 != 0:
        for j in range(side_length):
          if j%2 != 0:
            grid_img[i][j] = '+'
          else:
            grid_img[i][j] = '-'
      else:
        for j in range(side_length):
          if j%2 != 0:
            grid_img[i][j] = '|'
          else:
            i_in_actual_grid = int(i/2)
            j_in_actual_grid = int(j/2)
            grid_img[i][j] = self.grid_list[i_in_actual_grid][j_in_actual_grid]
    
    for i in range(side_length):
      for j in range(side_length):
        print(grid_img[i][j],end='')
      print()
    del grid_img

  # def __eq__(self, __o: object) -> bool:
  #   pass

  def __eq__(self, other) -> bool:
    return isinstance(other,TicTacToe_Grid_State) and self.grid_list == other.grid_list
  def __lt__(self,other) -> bool:
    return isinstance(other,TicTacToe_Grid_State) and True




class Agent:
  def __init__(self,m = 3) -> None:
    self.length_of_tic_tac_toe = m
    self.current_state = self.initial_state_of_every_game()
    self.depth = 0
    self.depth_count = 0
    self.number_of_leaves_of_the_game_tree_explored = 0
    self.number_of_leaves_of_the_game_tree_explored_for_minimax = 0
    self.number_of_leaves_of_the_game_tree_explored_for_alpha_beta = 0
    self.alpha = -10
    # highest value before searching 
    self.beta = 10
    # lowest value before searching

    self.max_depth_minimax = 0
    self.max_depth_alpha_beta = 0

  def initial_state_of_every_game(self) -> TicTacToe_Grid_State:
    grid_list = [
      [' ' for _ in range(self.length_of_tic_tac_toe)] for _ in range(self.length_of_tic_tac_toe)
    ]
    return TicTacToe_Grid_State(grid_list)


  def child_generator(self,current_state: TicTacToe_Grid_State, current_player_max = True):
    # copy_current_state = copy.deepcopy(current_state)
    vacant_pos_list = current_state.find_num_of_vacant_positions()

    # print(vacant_pos_list)
    # not modifying vacant_pos_list

    
    # children_states = [
    #   copy.deepcopy(current_state) for _ in range(len(vacant_pos_list))
    # ]
    children_states = [
      TicTacToe_Grid_State(current_state.grid_list) for _ in range(len(vacant_pos_list))
    ]
    if current_player_max:
      for i in range(len(vacant_pos_list)):
        (x,y) = vacant_pos_list[i]
        child_state = children_states[i]
        child_state.grid_list[x][y] = 'X'
    else:
      for i in range(len(vacant_pos_list)):
        (x,y) = vacant_pos_list[i]
        child_state = children_states[i]
        child_state.grid_list[x][y] = 'O'

    # for child_state in children_states:
    #   child_state.print_current_grid_state()
    #   print(self.isTerminal_state(child_state))
    return children_states

  def input_state_from_min_player(self) -> TicTacToe_Grid_State:
    position = int(input())
    grid_list = copy.deepcopy(self.current_state.grid_list)
    while position not in range(self.length_of_tic_tac_toe * self.length_of_tic_tac_toe) or grid_list[int(position/self.length_of_tic_tac_toe)][position%self.length_of_tic_tac_toe] != ' ':
      print('Invalid input')
      position = (int(input()))
    (x,y) = (int(position/self.length_of_tic_tac_toe),position%self.length_of_tic_tac_toe)

    grid_list[x][y] = 'O'
    new_state = TicTacToe_Grid_State(grid_list)
    # new_state.print_current_grid_state()
    return new_state
    
    


  def start_game_minimax(self):
    self.max_depth_minimax = 0
    self.number_of_leaves_of_the_game_tree_explored = 0
    m = self.length_of_tic_tac_toe
    instruction_list = [
      [i + j*m for i in range(m)] for j in range(m)
    ]
    instruction_state = TicTacToe_Grid_State(instruction_list)
    instruction_state.print_current_grid_state()
    del instruction_state
    depth = 0



    while not self.isTerminal_state(self.current_state):
      print('Enter postion for O player')
      print()
      print()
      self.current_state = self.input_state_from_min_player()
      # print('the grid after player\'s input is ')
      self.current_state.print_current_grid_state()
      if self.isTerminal_state(self.current_state):
        break
      print()
      print()
      # self.current_state,depth = self.minimax_decision(self.current_state)
      (max_state,depth) = self.minimax_decision(self.current_state)
      
      if depth > self.max_depth_minimax:
        self.max_depth_minimax = depth

      max_state: TicTacToe_Grid_State
      self.current_state = max_state
      
      # print(f'The min value is {self.min_value(self.current_state)}')
      self.current_state: TicTacToe_Grid_State
      self.current_state.print_current_grid_state()

    
    final_utility = self.utility_of_terminal_state(self.current_state)
    if final_utility == 0:
      print('the game ends in a draw')
    elif final_utility == 1:
      print('Agent won')
    else:
      print('You won')
    # self.max_depth_minimax = depth
    self.number_of_leaves_of_the_game_tree_explored_for_minimax = self.number_of_leaves_of_the_game_tree_explored
  def start_game_alpha_beta(self):
    self.max_depth_alpha_beta = 0

    self.current_state = self.initial_state_of_every_game()
    self.number_of_leaves_of_the_game_tree_explored = 0
    m = self.length_of_tic_tac_toe
    instruction_list = [
      [i + j*m for i in range(m)] for j in range(m)
    ]
    instruction_state = TicTacToe_Grid_State(instruction_list)
    instruction_state.print_current_grid_state()
    del instruction_state
    while not self.isTerminal_state(self.current_state):
      print('Enter postion for O player')
      print()
      print()
      self.current_state = self.input_state_from_min_player()
      print('the grid after player\'s input is ')

      self.current_state.print_current_grid_state()
      if self.isTerminal_state(self.current_state):
        # print('Terminal state reached')
        break
      print()
      print()

      max_state, depth = self.alpha_beta_search(self.current_state)

      max_state: TicTacToe_Grid_State

      if depth > self.max_depth_alpha_beta:
        self.max_depth_alpha_beta = depth


      # self.current_state = self.alpha_beta_search(self.current_state)
      
      self.current_state = max_state

      self.current_state.print_current_grid_state()

    
    final_utility = self.utility_of_terminal_state(self.current_state)
    if final_utility == 0:
      print('the game ends in a draw')
    elif final_utility == 1:
      print('Agent won')
    else:
      print('You won')
    
    self.number_of_leaves_of_the_game_tree_explored_for_alpha_beta = self.number_of_leaves_of_the_game_tree_explored
    


  def isTerminal_state(self, grid_state: TicTacToe_Grid_State,print_grid = False) -> bool:
    m = grid_state.grid_side_length
    # print(m)
    # check rows
    if(print_grid):
      grid_state.print_current_grid_state()

    for row in grid_state.grid_list:
      if row.count('X') == m or row.count('O') == m:
        self.number_of_leaves_of_the_game_tree_explored += 1
        return True
    
    # column checking
    for i in range(m):
      column = [
        grid_state.grid_list[j][i] for j in range(m)
      ]
      # if print_grid:
      #   print(column)
      if column.count('X') == m or column.count('O') == m:
        self.number_of_leaves_of_the_game_tree_explored += 1
        return True

    # diagonals
    diagonal1 = [
      grid_state.grid_list[i][i] for i in range(m)
    ]
    if diagonal1.count('X') == m or diagonal1.count('O') == m:
      self.number_of_leaves_of_the_game_tree_explored += 1
      return True
    # diagonal1 is a new list
    del diagonal1

    diagonal2 = [
      grid_state.grid_list[i][m-i-1] for i in range(m)
    ]
    if diagonal2.count('X') == m or diagonal2.count('O') == m:
      self.number_of_leaves_of_the_game_tree_explored += 1
      return True
    del diagonal2

    for i in range(m):
      for j in range(m):
        if grid_state.grid_list[i][j] == ' ':
          return False
        

    return True
  

  def utility_of_terminal_state(self, grid_state: TicTacToe_Grid_State) -> int:
    m = grid_state.grid_side_length
    # print(m)
    # check rows
    for row in grid_state.grid_list:
      if row.count('X') == m:
        return 1
      elif row.count('O') == m:
        return -1
    
    # column checking
    for i in range(m):
      column = [
        grid_state.grid_list[j][i] for j in range(m)
      ]
      if column.count('X') == m:
        return 1
      elif column.count('O') == m:
        return -1
      

    # diagonals
    diagonal1 = [
      grid_state.grid_list[i][i] for i in range(m)
    ]
    if diagonal1.count('X') == m:
      return 1
    elif diagonal1.count('O') == m:
      return -1
    # diagonal1 is a new list
    del diagonal1

    diagonal2 = [
      grid_state.grid_list[i][m-i-1] for i in range(m)
    ]
    if diagonal2.count('X') == m:
      return 1
    elif diagonal2.count('O') == m:
      return -1
    del diagonal2

    return 0
  
  def minimax_decision(self, grid_state: TicTacToe_Grid_State) -> tuple:
    self.depth_count = 0
    children_states = self.child_generator(grid_state,current_player_max=True)
    # children_states_utility_values = [
    #   self.min_value(child_state) for child_state in children_states
    # ]
    children_states_utility_values = []
    depth_list = []

    for i in range(len(children_states)):
      child_state = children_states[i]
      utility_to_be_appended, depth = self.min_value(child_state)
      children_states_utility_values.append(utility_to_be_appended)
      depth_list.append(depth)
      

    # max_value_of_utility = max(children_states_utility_values)
    # index_of_max_value = children_states_utility_values.index(max_value_of_utility)

    # sorted_list = [
    #   (utility,child_state) for utility,child_state in (zip(children_states_utility_values,children_states))
    # ]
    # when using sorted(zip(...))
    # correct output was not coming for max player
    # sorted_list.sort()

    

    max_value_of_utility = max(children_states_utility_values)
    for i in range(len(children_states)):
      if children_states_utility_values[i] == max_value_of_utility:
        depth_max = max(depth_list)
        del depth_list
        return children_states[i],depth_max


    # for x in sorted_list:
      # print(x)
      # x[1].print_current_grid_state()
    # max(sorted_list)[1].print_current_grid_state()
    # return max(sorted_list)[1]
    # return sorted_list[-1][1]
    # return max_state
  
  

  def min_value(self, grid_state: TicTacToe_Grid_State) -> tuple:
    # print('inside max_value')
    # self.depth_count +=1 
    if self.isTerminal_state(grid_state):
      return self.utility_of_terminal_state(grid_state),1
    # v = -10
    # simulating negative infinity
    v = 10

    depth_list = []

    children_states = self.child_generator(grid_state,current_player_max = False)
    # children_states = self.child_generator(grid_state,current_player_max = True)
    for child_state in children_states:
      # print('in max-value')
      # child_state.print_current_grid_state()

      current_utility, depth = self.max_value(child_state)

      # v,depth = min(v, self.max_value(child_state))
      v = min(v,current_utility)
      depth_list.append(1 + depth)
    del children_states
    depth_max = max(depth_list)
    del depth_list

    return v,depth_max

  def max_value(self, grid_state: TicTacToe_Grid_State) -> tuple:
    # self.depth_count = 
    # print('inside min_value')
    # print('of')
    # grid_state.print_current_grid_state()
    if self.isTerminal_state(grid_state):
      return self.utility_of_terminal_state(grid_state),1
    # v = 10
    # simulating positive infinity
    v = -10
    children_states = self.child_generator(grid_state,current_player_max = True)
    # children_states = self.child_generator(grid_state,current_player_max = False)
    depth_list = []
    for child_state in children_states:
      # print('in min-value')
      # child_state.print_current_grid_state()

      current_utility, depth = self.min_value(child_state)
      # (v,depth) = max(v, self.min_value(child_state))
      v = max(v,current_utility)
      depth_list.append(1 + depth)

    del children_states
    depth_max = max(depth_list)
    del depth_list


    return v,depth_max




  def alpha_beta_search(self, grid_state: TicTacToe_Grid_State) -> TicTacToe_Grid_State:
    # self.alpha = -10
    # self.beta = 10
    alpha=-1
    beta=1
    self.depth_count = 0
    children_states = self.child_generator(grid_state,current_player_max=True)

    v = -1
    
    # children_states_utility_values = [
    #   self.min_value_alpha_beta(child_state,alpha,beta) for child_state in children_states
    # ]

    utiltity_values = []

    depth_list = []
    depth_max = 0
    for i in range(len(children_states)):
      current, depth = self.min_value_alpha_beta(children_states[i],alpha,beta)

      depth_list.append(depth)

      v = max(v, current)
      utiltity_values.append(v)
      if v > alpha:
        alpha = v
      if current > beta:
        
        depth_max = max(depth_list)
        del depth_list
        return children_states[i-1], depth_max
      

    if depth_list:
      depth_max = max(depth_list)
      del depth_list
    
    # how is it working 
    utiltity_max = max(utiltity_values)
    for i in range(len(utiltity_values)):
      if utiltity_values[i] == utiltity_max:
        return children_states[i],depth_max



    # for child_state in children_states:
    #   current = self.min_value_alpha_beta(child_state,alpha,beta)
    #   v = max(v,current)
    #   if v > alpha:
    #     alpha = v
    #   if current > beta:
    #     return child_state

    # max_value_of_utility = max(children_states_utility_values)
    # for i in range(len(children_states)):
    #   if children_states_utility_values[i] == max_value_of_utility:
    #     return children_states[i]

  def max_value_alpha_beta(self, grid_state: TicTacToe_Grid_State,alpha,beta) -> int:
    if self.isTerminal_state(grid_state):
      return self.utility_of_terminal_state(grid_state),1
    v = -10
    # simulating negative infinity
    # children_states = self.child_generator(grid_state,current_player_max = False)
    children_states = self.child_generator(grid_state,current_player_max = True)

    depth_list = []
    depth_max = 0

    for child_state in children_states:
      current,depth = self.min_value_alpha_beta(child_state,alpha,beta)
      depth_list.append(1 + depth)

      v = max(v, current)

      if v > alpha:
        alpha = v
      if current > beta:
        depth_max = max(depth_list)
        del depth_list


        del children_states

        return current, depth_max

    if children_states:
      del children_states
    
    if depth_list:
      depth_max = max(depth_list)
      del depth_list

    return v,depth_max
  
  def min_value_alpha_beta(self, grid_state: TicTacToe_Grid_State,alpha,beta) -> int:
    # self.depth_count = 
    # print('inside min_value')

    if self.isTerminal_state(grid_state):
      return self.utility_of_terminal_state(grid_state),1
    v = 10
    # simulating positive infinity
    # children_states = self.child_generator(grid_state,current_player_max = True)
    children_states = self.child_generator(grid_state,current_player_max = False)
    # is it True ??????????

    depth_list = []
    depth_max = 0
    for child_state in children_states:
      current, depth =self.max_value_alpha_beta(child_state,alpha,beta)
      depth_list.append(1 + depth)
      v = min(v, current)
      if v<beta:
        beta=v
      if current<alpha:
        del children_states

        depth_max = max(depth_list)
        del depth_list
        return current,depth_max
    
    if depth_list:
      depth_max = max(depth_list)
      del depth_list

    if children_states:
      del children_states
    return v, depth_max


# sample_grid = TicTacToe_Grid_State([[' ',' ',' '],[' ','O',' '],[' ',' ',' ']])



# *************************
# sample_grid2 = TicTacToe_Grid_State(copy.deepcopy([['O',' ',' '],[' ',' ',' '],['O',' ',' ']]))
# print(sample_grid == sample_grid2)

# *******************
# sample_grid.print_current_grid_state()
# print('--------------')

# agent = Agent()
# sample_grid.print_current_grid_state()
# print('initial state is ')
# print(agent.min_value_alpha_beta(sample_grid))

# children = agent.child_generator(sample_grid,current_player_max=True)
# # agent.alpha = -10
# # agent.beta = 10
# print('the children states are ')
# for x in children:
#   x: TicTacToe_Grid_State
#   print()
#   x.print_current_grid_state()
#   print(agent.max_value_alpha_beta(x))
#   print()

# agent.alpha_beta_search(sample_grid).print_current_grid_state()











agent = Agent()
agent.number_of_leaves_of_the_game_tree_explored = 0

agent.start_game_minimax()

minimax_explored_leaves = agent.number_of_leaves_of_the_game_tree_explored
print(f'the number of leaves of game tree explored is {agent.number_of_leaves_of_the_game_tree_explored}')
print()
print(f'the maximum depth is {agent.max_depth_minimax}')


agent.start_game_alpha_beta()
print(f'the number of leaves of game tree explored in alpha beta is {agent.number_of_leaves_of_the_game_tree_explored}')
print()
print(f'the maximum depth is {agent.max_depth_alpha_beta}')


alpha_beta_leaves = agent.number_of_leaves_of_the_game_tree_explored

print(f'ALPHA BETA PRUNING searches {alpha_beta_leaves} leaves whereas MINIMAX searches {minimax_explored_leaves} leaves')

print(f'Alpha Beta pruning is {minimax_explored_leaves/alpha_beta_leaves} times efficient than minimax')
