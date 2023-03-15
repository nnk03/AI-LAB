import copy
import random as rnd


class TicTacToe_Grid:
  def __init__(self, grid:list ,length = 3, maxPlayer=True, minPlayer=False) -> None:

    self.player = 'M' if maxPlayer else 'm'
    self.grid_list = grid
    self.length = length
    # self.isTerminal_state = self.determine_if_terminal_state()

  def determine_if_terminal_state(self):
    grid = self.grid_list
    for i in range(self.length):
      if self.isConsecutive(grid[i]):
        return True
    
    for j in range(self.length):
      column_list = list([
        grid[i][j] for i in range(self.length)
      ])
      if self.isConsecutive(column_list):
        return True
      del column_list
    
    diagonal_1 = list([
      grid[i][i] for i in range(self.length)
    ])
    if self.isConsecutive(diagonal_1):
      return True
    
    del diagonal_1

    diagonal_2 = list([
      grid[i][self.length - i - 1] for i in range(self.length)
    ])
    if self.isConsecutive(diagonal_2):
      return True
    
    return False

  def isConsecutive(self,row_column_diagonal: list):
    ch = row_column_diagonal[0]
    if ch=='X' or ch=='O':
      if row_column_diagonal.count(ch) == len(row_column_diagonal):
        return True
    return False

  def print_grid(self):
    side_length = 2*self.length - 1
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

  def index_to_number(self, i:int, j:int):
    return i*self.length + j + 1

  def number_to_index(self, number: int):
    return (
      int((number-1)/self.length),
      int((number-1)%self.length)
    )


class Agent:
  def __init__(self,in_game_grid: list) -> None:
    self.in_game_grid = list(in_game_grid)
    self.length_of_puzzle = len(in_game_grid)
    current_list = [
      [' ' for _ in range(self.length_of_puzzle)] for _ in range(self.length_of_puzzle)
    ]
    self.current_game_state = TicTacToe_Grid(current_list)

  def calculate_utility_of_terminal_grid(self,grid_state: TicTacToe_Grid):
    grid_list = grid_state.grid_list
    # first calculating for 3 X's or 3 Y's
    # not 3 consecutive
    # first assuming 3x3 

    # instead of 3 replace with length of the list which we are considering
    m = grid_state.length
    for lst in grid_list:
      lst: list
      if lst.count('X') == 3:
        return 1
      elif lst.count('O') == 3:
        return -1
      else:
        continue
    for i in range(m):
      column = list([
        # string is immutable
        grid_list[i][j] for j in range(m)
      ])
      if column.count('X') == 3:
        del column
        return 1
      elif column.count('O') == 3:
        del column
        return -1
      else:
        del column
        continue
    
    # diagonal elements
    diagonal1 = [
      grid_list[i][i] for i in range(m)
    ]
    if diagonal1.count('X') == 3:
      del diagonal1
      return 1
    elif diagonal1.count('O') == 3:
      del diagonal1
      return -1
    del diagonal1
    diagonal2 = [
      grid_list[i][m-1-i] for i in range(m)
    ]
    if diagonal2.count('X'):
      del diagonal2
      return 1
    elif diagonal2.count('O') == 3:
      del diagonal2
      return -1
    del diagonal2


    return 0

  def vacant_space_in_the_grid(self,grid_state: TicTacToe_Grid):
    vacant_space_list = []
    m = grid_state.length
    grid_list = grid_state.grid_list
    for i in range(m):
      for j in range(m):
        if grid_list[i][j] == ' ':
          vacant_space_list.append((i,j))
    return vacant_space_list
  
  def child_generator_from_current_state(self,grid_state: TicTacToe_Grid):
    vacant_space_list = self.vacant_space_in_the_grid(grid_state)
    grid_list = grid_state.grid_list.copy()
    children_list = []
    for (i,j) in vacant_space_list:
      # grid_list_copy = list(grid_list)
      grid_list_copy = copy.deepcopy(grid_list)
    
      grid_list_copy[i][j] = 'X'
      
      children_list.append(grid_list_copy)
    children_states = [
      TicTacToe_Grid(child_grid_list) for child_grid_list in children_list
    ]
    # for child in children_states:
    #   print()
    #   child.print_grid()
    #   print()
    return children_states
  
  def minimax_decision(self,grid_state: TicTacToe_Grid) -> TicTacToe_Grid:
    # input is a state
    # if grid_state.determine_if_terminal_state():
    #   if 
    # in this funciton, we have to make sure that terminal state does not reach here
    children_states = self.child_generator_from_current_state(grid_state)
    utility_list = [
      self.min_value(child_state) for child_state in children_states
    ]
    maximising_min_value = max(utility_list)
    index = utility_list.index(maximising_min_value)
    return children_states[index]

  def max_value(self,grid_state: TicTacToe_Grid) -> int:
    if grid_state.determine_if_terminal_state():
      return self.calculate_utility_of_terminal_grid(grid_state)
    # utility_of_children_list = []
    utility = -10
    # similar to negative infinity in the algorithm
    # since utility never takes any other values other than -1,0,1
    children_states = self.child_generator_from_current_state(grid_state)
    for child_state in children_states:
      utility = max(utility,self.min_value(child_state))
    return utility

  def min_value(self,grid_state: TicTacToe_Grid) -> int:
    if grid_state.determine_if_terminal_state():
      return self.calculate_utility_of_terminal_grid(grid_state)
    utility = 10
    # similar to positive infinity in the algorithm
    # since utility never takes any other values other than -1,0,1
    children_states = self.child_generator_from_current_state(grid_state)
    for child_state in children_states:
      utility = min(utility,self.max_value(child_state))
    return utility

  def ask_min_player_input(self) -> tuple:
    input_position = int(input('enter position for \'O\' player: '))
    m = self.length_of_puzzle
    i = int(input_position / m)
    j = int(input_position % m)
    return (i,j)
  
  def min_player_input_and_max_player_output(self,grid_state: TicTacToe_Grid):
    i,j = self.ask_min_player_input()
    # print(i,j)
    m = self.length_of_puzzle
    grid_list = grid_state.grid_list
    while i not in range(m) or j not in range(m) or grid_list[i][j] != ' ':
      print('Wrong Input... Try Again')
      i,j = self.ask_min_player_input()
    
    grid_list_copy = copy.deepcopy(grid_list)
    grid_list_copy[i][j] = 'O'
    # self.current_game_state = TicTacToe_Grid(grid_list_copy,length=m)
    # self.current_game_state.print_grid()
    current_game_state = TicTacToe_Grid(grid_list_copy,length=m)
    current_game_state.print_grid()
    if self.current_game_state.determine_if_terminal_state():
      return False,current_game_state
    else:
      output_state = self.minimax_decision(self.current_game_state)
      output_state.print_grid()
      return True,output_state


  def start_game(self):

    while True:
      current_state = self.current_game_state
      if current_state.determine_if_terminal_state():
        utility = self.calculate_utility_of_terminal_grid(current_state)
        if utility == 1:
          print('Player X won')
        elif utility == -1:
          print('Player O won. Agent lost')
        else:
          print('Game ended in a draw')
        # to break the while loop
        break

      output_state = self.min_player_input_and_max_player_output(current_state)

      output_state_1 = output_state[1]

      if output_state_1.determine_if_terminal_state():
        utility = self.calculate_utility_of_terminal_grid(output_state_1)
        if utility == 1:
          print('Player X won')
        elif utility == -1:
          print('Player O won. Agent lost')
        else:
          print('Game ended in a draw')
        # to break the while loop
        break

      self.current_game_state = output_state[1]





class Tic_Tac_Toe_Game:
  def __init__(self,length=3) -> None:
    self.length_of_puzzle = length
    grid = [
      list(['' for _ in range(length)]) for _ in range(length)
    ]
    self.game_grid = grid

  def print_location_grid(self):
    grid = self.game_grid
    minPlayer_turn = True
    maxPlayer_turn = False
    m = self.length_of_puzzle
    img_to_be_printed_initially = [
      [i + m*j for i in range(m)] for j in range(m)
    ]
    game_start_instruction_grid = TicTacToe_Grid(img_to_be_printed_initially,length=m)
    print('Board locations are as follows')
    print()
    game_start_instruction_grid.print_grid()
    print()
    del game_start_instruction_grid
    # while True:

  # def min_player_turn(self):


game = Tic_Tac_Toe_Game()
game.print_location_grid()

agent = Agent(game.game_grid)
agent.start_game()

# mylst = [
#   ['X',2,3],
#   [4,'X',6],
#   [7,8,'X']
# ]

# grid = TicTacToe_Grid(mylst)
# grid.print_grid()
