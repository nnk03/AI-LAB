# 
import pandas as pd
import numpy as np
import re
import random as rnd


class RoomFloor:

  def __init__(self,m,n,numRandomDirt) -> None:
    self.rows = m
    self.columns = n
    self.clock = 0
    self.floorGrid = [[0 for _ in range(n)] for _ in range(m)]
    self.numDirtPlaces = 0
    while self.numDirtPlaces != numRandomDirt:
      i = rnd.randint(0,m-1)
      j = rnd.randint(0,n-1)
      if self.floorGrid[i][j] != 1:
        self.floorGrid[i][j] = 1
        self.numDirtPlaces += 1
  
  def addDirt(self,i,j):
    self.floorGrid[i][j] += 1
  
  def printCurrentState(self,x,y):
    for i in range(self.rows):
      for j in range(self.columns):
        if i==x and y==j:
          print(f'{self.floorGrid[i][j]},X',end='     ')
        else:
          print(f'{self.floorGrid[i][j]}',end='       ')
        # is there a function to add padding???
      print()


  def isClean(self):
    for row in self.floorGrid:
      for value in row:
        if value != 0:
          return False
    return True

  




roomFloor = RoomFloor(5,5,10)
# roomFloor.printCurrentState(1,2)
# print(roomFloor.isClean())

class CleaningAgent:

  def __init__(self) -> None:
    self.score = 0

  



