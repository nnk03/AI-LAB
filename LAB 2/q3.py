# 
import pandas as pd
import numpy as np
import re
import random as rnd


# we have to use random.choices()
# difference between weights and cumulative weights

# 1a
class Player:
  def __init__(self,x) -> None:
    # x represents actual index
    self.ith_player_tuple = (x,x+1)
    self.runs = 0
    self.possibleShots = [1,2,3,4,6]
    self.isOutYet = False

    w = 11-x
    pOutMax = [0.1,0.2,0.3,0.5,0.7]
    pOutMin = [0.01,0.02,0.03,0.1,0.3]

    if x == 1:
      # the reason for if else statement is that python is approximating (w-1)/9
      self.pOutList = pOutMin
    elif x==10:
      self.pOutList = pOutMax
    else:
      self.pOutList = [
        pOutMax[i] - (pOutMax[i] - pOutMin[i])*(w - 1)/9
        for i in range(5)
      ]
    
    pRunMin = 0.5
    pRunMax = 0.8

    if w==1:
      # similar reason as that of previous if else
      self.pRun = pRunMin
    elif w==10:
      self.pRun = pRunMax
    else:
      self.pRun = pRunMin + (pRunMax - pRunMin) * (w-1)/9

  def print_pOut(self):
    print(self.pOutList)
  
  def print_pRun(self):
    print(self.pRun)

  def print_runs(self):
    print(self.runs)

  def printCurrentStateOfPlayer(self):
    out = 'out' if self.isOutYet else 'not out'
    print()
    print(f'The player is {self.ith_player_tuple}')
    print(f'The Probability pOut = {self.pOutList}')
    print(f'The possible shots are {self.possibleShots}')
    print(f'The probability pRun = {self.pRun}')
    print(f'The runs scored by this player is {self.runs}')
    print(f'The player is {out}')
    print()


    # self.pOut = pOutList

  # def pOut(self):






class ODI:
  def __init__(self) -> None:
    # total number of balls
    self.balls = 300
    # balls left
    self.ballsLeft = 300
    # all possible shots
    self.shots = [1,2,3,4,6]
    # start state
    self.startState = (300,10)
    # current State
    self.currentState = (300,10)
    # clock to track the number of balls, if a ball is thrown, then the clock increments by 1  
    self.totalRuns = 0
    self.clock = 0
    self.pOutMin = [0.01,0.02,0.03,0.1,0.3]
    
    self.pOutMax = [0.1,0.2,0.3,0.5,0.7]
    self.wicketsInHand = 10
    self.currentPlayer = 11 - self.wicketsInHand
    self.players = [ Player(i+1) for i in range(10) ]
    

  def print_pOut_ofAllPlayers(self):
    for player in self.players:
      player.print_pOut()
    # print(len(self.players))
  def print_pRun_ofAllPlayers(self):
    for player in self.players:
      player.print_pRun()

  def ballPlayed(self,wicketsInHand):

    # if a ball is played, then the state changes

    


    self.ballsLeft -= 1
    self.clock += 1
    self.currentState = (self.ballsLeft,wicketsInHand)

  def printCurrentStateOfOdi(self):
    print()
    print(f'The number of balls played is {self.clock}')
    print(f'The number of balls left is {self.ballsLeft}')
    print(f'The current state is {self.currentState}')
    print(f'the current player is {self.players[self.currentPlayer - 1].ith_player_tuple}')
    print(f'the number of wickets in hand is {self.wicketsInHand}')
    print()
    for player in self.players:
      player.printCurrentStateOfPlayer()
    print()


odi = ODI()


# 1a
def playBall(odi: ODI,a_t = 0,currentPlayer = odi.currentPlayer):
  a_t = int(input()) if a_t == 0 else a_t
  if a_t==5:
    print('no such run')
  else:
    indexOfShot = odi.shots.index(a_t)
    # player = odi.players[11-odi.wicketsInHand-1]
    player = odi.players[currentPlayer - 1]
    player.printCurrentStateOfPlayer()
    pOut = player.pOutList[indexOfShot]
    # since player is call by reference, we don't need to update the state
    pOut = [pOut, 1-pOut]
    isOut = rnd.choices([True,False],cum_weights=pOut,k=1)
    # isOut contains a list 
    isOut = isOut[0]
    if isOut:
      wicketsInHand = odi.wicketsInHand - 1
      player.isOutYet = True
      odi.currentPlayer += 1 
      odi.ballPlayed(wicketsInHand)
    else:
      # print(f'************ {player.isOutYet} *************')
      if not player.isOutYet:
        odi.ballPlayed(odi.wicketsInHand)
        pRun = player.pRun
        probRun = [pRun,1-pRun]
        doesScore = rnd.choices([True,False],cum_weights=probRun,k=1)
        # doesScore is a list
        doesScore = doesScore[0]
        # print(doesScore)
        # doesScore is a boolean representing whether the player scored or was it a dot ball
        if doesScore:
          # if the player scored, update the runs and return the score
          odi.totalRuns += a_t
          player.runs += a_t
          return a_t
        else:
          return 0
      

# odi.printCurrentStateOfOdi()


# print(odi.currentState, odi.totalRuns)
# playBall(odi)
# print(odi.currentState, odi.totalRuns)
print(odi.currentState,odi.totalRuns,odi.currentPlayer)
i = 0
while i<300 and odi.currentPlayer <=10 :
  playBall(odi,rnd.choices(odi.shots,k=1)[0])
  print(odi.currentState,odi.totalRuns,odi.currentPlayer)
  i+=1










# odi.print_pOut_ofAllPlayers()
# odi.print_pRun_ofAllPlayers()