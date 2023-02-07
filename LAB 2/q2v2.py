# 

import pandas as pd
import numpy as np
import re
import random as rnd

# 2a
class RoomFloor:
  def __init__(self,m,n) -> None:
    self.floorClock = 1
    self.isClean = False
    self.rows = m
    self.columns = n
    self.floorGrid = [
      [0 for _ in range(n)] for _ in range(m)
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
    self.floorClock += 1

  def addDirt(self):
    y = rnd.randint(0,self.rows-1)
    x = rnd.randint(0,self.columns - 1)
    # self.clock += 1
    self.updateClock()
    self.floorGrid[y][x] += 1

  def print_state_of_floor(self):
    print()
    print(f'clock of floor is {self.floorClock}')
    for row in self.floorGrid:
      for tile in row:
        print(f'  {tile}  ',end=' ')
      print()
    
    print()

  def hasDirt_at_xy(self,x,y) -> bool:
    if self.floorGrid[y][x] != 0:
      return True
    return False



class Agent():

  def __init__(self,roomFloor: RoomFloor) -> None:
    self.agentClock = 1
    self.inRoomFloor = roomFloor
    self.loc = [0,0]
    # [x,y]
    self.actionList = ['up','down','left','right','pickDirt']
    self.currentAction = rnd.choices(
      self.actionList,
      k=1
    )[0]
    self.reward = self.calc_reward(self.currentAction,self.loc,self.inRoomFloor)
    

  def calc_reward(self,action:str,loc:list,roomFloor: RoomFloor) -> int:

    x = loc[0]
    y = loc[1]
    if action == 'pickDirt':
      if roomFloor.hasDirt_at_xy(x,y):
        amountOfDirt = roomFloor.floorGrid[y][x]
        roomFloor.floorGrid[y][x] = 0
        return amountOfDirt
      else:
        return -1
    elif action == 'up':
      if y==0:
        return -10
      else:
        # self.loc[1] -= 1

        # to move up the list , we have to decrease 1
        return 0
    elif action == 'down':
      if y==roomFloor.rows - 1:
        return -10
      else:
        # self.loc[1] += 1
        return 0
    elif action == 'left':
      if x==0:
        return -10
      else:
        # self.loc[0] -= 1
        return 0
    else:
      if x == roomFloor.columns - 1:
        return -10
      else:
        # self.loc[0] += 1
        return 0
    
  def change_position(self,action:str,loc:list,roomFloor: RoomFloor) -> None:
    x = loc[0]
    y = loc[1]
    if action == 'pickDirt':
      if roomFloor.hasDirt_at_xy(x,y):
        amountOfDirt = roomFloor.floorGrid[y][x]
        roomFloor.floorGrid[y][x] = 0
        # return amountOfDirt
      # else:
      #   return -1
    elif action == 'up':
      if y==0:
        pass
        # return -10
      else:
        self.loc[1] -= 1

        # to move up the list , we have to decrease 1
        # return 0
    elif action == 'down':
      if y==roomFloor.rows - 1:
        # return -10
        pass
      else:
        self.loc[1] += 1
        # return 0
    elif action == 'left':
      if x==0:
        # return -1
        pass
      else:
        self.loc[0] -= 1
        # return 0
    else:
      if x == roomFloor.columns - 1:
        # return -10
        pass
      else:
        # return 0
        self.loc[0] += 1



  def print_state_of_agent(self):
    print()
    print(f'The current location of agent is {self.loc}')
    print(f'The current action of agent is {self.currentAction}')
    print(f'The reward obtained is {self.reward}')
    print()

  def doAction_modifyReward(self):
    self.change_position(action=self.currentAction,loc=self.loc,roomFloor=self.inRoomFloor)
    self.currentAction = rnd.choices(
      self.actionList,
      k=1
    )[0]
    self.reward = self.calc_reward(self.currentAction,self.loc,self.inRoomFloor)
    floor = self.inRoomFloor
    floor.addDirt()
    self.agentClock = floor.floorClock





m=int(input())
n=int(input())

roomFloor = RoomFloor(m,n)
# roomFloor.print_state_of_floor()

agent = Agent(roomFloor)
count = 0
while count < 10:
  roomFloor.print_state_of_floor()
  agent.print_state_of_agent()
  agent.doAction_modifyReward()
  count += 1

# count = 0
# while count < 10:
#   roomFloor.print_state_of_floor()
#   roomFloor.addDirt()
#   count += 1