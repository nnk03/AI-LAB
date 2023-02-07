# 
import pandas as pd
import numpy as np
import re
import random as rnd


# class RoomFloor:

#   def __init__(self,m,n,numRandomDirt) -> None:
#     self.rows = m
#     self.columns = n
#     self.clock = 0
#     self.floorGrid = [[0 for _ in range(n)] for _ in range(m)]
#     self.numDirtPlaces = 0
#     while self.numDirtPlaces != numRandomDirt:
#       i = rnd.randint(0,m-1)
#       j = rnd.randint(0,n-1)
#       if self.floorGrid[i][j] != 1:
#         self.floorGrid[i][j] = 1
#         self.numDirtPlaces += 1
  
#   def addDirt(self,i,j):
#     self.floorGrid[i][j] += 1
  
#   def printCurrentState(self,x,y):
#     for i in range(self.rows):
#       for j in range(self.columns):
#         if i==x and y==j:
#           print(f'{self.floorGrid[i][j]},X',end='     ')
#         else:
#           print(f'{self.floorGrid[i][j]}',end='       ')
#         # is there a function to add padding???
#       print()


#   def isClean(self):
#     for row in self.floorGrid:
#       for value in row:
#         if value != 0:
#           return False
#     return True




# roomFloor = RoomFloor(5,5,10)
# # roomFloor.printCurrentState(1,2)
# # print(roomFloor.isClean())

# class CleaningAgent:

#   def __init__(self) -> None:
#     self.score = 0



# 2a
class RoomFloor:
  def __init__(self,m,n) -> None:
    self.clock = 1
    self.isClean = False
    self.rows = m
    self.columns = n
    self.floorGrid = [
      [0 for i in range(n)] for j in range(m)
    ]
    # initialize 10 random locations to 1
    numDirtPlaces = 0
    while numDirtPlaces < 10:
      i = rnd.randint(0,m-1)
      j = rnd.randint(0,n-1)
      if self.floorGrid[i][j] == 0:
        self.floorGrid[i][j] = 1
        numDirtPlaces += 1

    
  def findIfClean(self) -> bool:
    for row in self.floorGrid:
      for element in row:
        if element != 0:
          return False
    return True

  def updateClock(self):
    self.clock += 1

  def addDirt(self):
    y = rnd.randint(0,self.rows-1)
    x = rnd.randint(0,self.columns - 1)
    # self.clock += 1
    self.updateClock()
    self.floorGrid[y][x] += 1

  def hasDirt_at_xy(self,x,y) -> bool :
    if self.floorGrid[y][x] != 0:
      return True
    return False





# 2b
class Agent():
  def __init__(self,roomFloor: RoomFloor) -> None:
    
    self.currentLocation = [0,0]
    self.inRoomFloor = roomFloor
    self.clock = roomFloor.clock
    self.actionList = ['up','down','right','left','pickDirt']
    # self.reward = 0
    
    # self.currentAction = ''
    self.currentAction = rnd.choices(
      self.actionList,
      k=1
    )[0]
    self.reward = self.findReward(self.currentAction,self.currentLocation,self.inRoomFloor)
    # action = self.currentAction
    # loc = self.currentLocation
    # floor = self.inRoomFloor
    
  def findReward(self,action:str,loc:list,floor:RoomFloor):
    if action == 'up':
      # self.currentLocation[1] -= 1
      # only if we decrement are we going up the list
      if loc[1] == 0:
        return -10
      else:
        # self.currentLocation[1] -= 1
        return 0
      
    elif action == 'down':
      
      if loc[1] == floor.rows - 1:
        return -10
      else:
        # self.currentLocation[1] += 1
        return 0
    elif action == 'left':
      
      if loc[0] == 0:
        return -10
      else:
        # self.currentLocation[0] -= 1
        return 0
    
    elif action == 'right':
      if loc[0] == floor.columns - 1:
        return -1
      else:
        # self.currentLocation[0] += 1
        return 0
    elif action=='':
      pass

    else:
      x = loc[0]
      y = loc[1]
      if floor.hasDirt_at_xy(x,y):
        # loc[1] is the x coordinate, loc[0] is the y-coordinate with respect to 2d list
        amountOfDirt = floor.floorGrid[y][x]
        floor.floorGrid[y][x] = 0
        return amountOfDirt
      else:
        return -1
  def updateClock(self):
    self.clock = self.inRoomFloor.clock
    # call this everytime after calling addDirt()

  def doAction_modifyReward(self):
    self.reward = self.findReward(self.currentAction,self.currentLocation,self.inRoomFloor)

    # randomIndex = rnd.randint(0,len(self.actionList)-1)
    # action = self.actionList[randomIndex]
    # floor = self.inRoomFloor
    # loc = self.currentLocation
    # print(loc)
    # self.currentAction = action
    action = self.currentAction
    loc = self.currentLocation
    floor = self.inRoomFloor
    print(loc,action)
    # self.reward = self.findReward(action,loc,floor)


    # do action and update reward
    # it is y,x and not x,y in 2d list
    if action == 'up':
      # self.currentLocation[1] -= 1
      # only if we decrement are we going up the list
      if loc[1] == 0:
        # self.reward = -10
        pass
      else:
        self.currentLocation[1] -= 1
        # self.reward = 0
      
    elif action == 'down':
      
      if loc[1] == floor.rows - 1:
        # self.reward = -10
        pass
      else:
        self.currentLocation[1] += 1
        # self.reward = 0
    elif action == 'left':
      
      if loc[0] == 0:
        # self.reward = -10
        pass
      else:
        self.currentLocation[0] -= 1
        # self.reward = 0
    
    elif action == 'right':
      if loc[0] == floor.columns - 1:
        # self.reward = -1
        pass
      else:
        self.currentLocation[0] += 1
        # self.reward = 0
    elif action=='':
      pass

    else:
      x = loc[0]
      y = loc[1]
      if floor.hasDirt_at_xy(x,y):
        # loc[1] is the x coordinate, loc[0] is the y-coordinate with respect to 2d list
        amountOfDirt = floor.floorGrid[y][x]
        floor.floorGrid[y][x] = 0
        # self.reward = amountOfDirt
      else:
        # self.reward = -1
        pass
    
    # after doing action, update the clock of agent and add Dirt on the floor (clock of floor is updated in the addDirt() function)
    action = rnd.choices(
      self.actionList,
      k=1
    )[0]
    self.currentAction = action

    floor.addDirt()
    # update clock of agent after adding Dirt
    self.updateClock()
  
  def print_state_agent_and_floor(self):
    floor = self.inRoomFloor
    floorGrid = floor.floorGrid
    loc = self.currentLocation
    print()
    print(f'The state of the grid at time={self.clock} is ')
    for row in floorGrid:
      for tile in row:
        print(f'  {tile}  ',end=' ')
      print()
    print()
    print(f'The Location of agent at time {self.clock} is {loc} ')
    print(f'The action of the agent is {self.currentAction}')
    print(f'The reward obtained is {self.reward}')
    print()


# 2c

m = int(input())
n = int(input())

roomFloor = RoomFloor(m,n)
agent = Agent(roomFloor)

time = 0
while time < 10:
  agent.print_state_agent_and_floor()
  agent.doAction_modifyReward()
  time += 1

