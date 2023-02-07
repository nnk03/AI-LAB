# 
import pandas as pd
import numpy as np
import re
import random as rnd

class Player:
  def __init__(self,index) -> None:
    # index is starting from 1
    self.indexOfPlayer = index
    self.player_tuple = (index,index+1)
    self.runs = 0
    self.isOut = False
    self.balls_played_by_thisPlayer = 0
    self.shots = [1,2,3,4,6]


    pOutMax = [0.1,0.2,0.3,0.5,0.7]
    pOutMin = [0.01,0.02,0.03,0.1,0.3]
    pOut = []
    if index==1:
      pOut = pOutMin
    elif index==10:
      pOut = pOutMax
    else:
      w = 11-index
      pOut = [
        pOutMax[i] - (pOutMax[i] - pOutMin[i])*(w-1)/9

        for i in range(5)
      ]
    
    self.pOutList = pOut

    pRunMin = 0.5
    pRunMax = 0.8
    if index==1:
      pRun = pRunMax
    elif index == 10:
      pRun = pRunMin
    else:
      w = 11 - index
      pRun = pRunMin + (pRunMax - pRunMin)*(w-1)/9
    self.pRun = pRun

  # for debugging purpose
  # printing the info of this player
  def print_state_of_player(self):
    print(f'the player index is {self.indexOfPlayer}')
    print(f'player is {self.player_tuple}')
    print(f'Runs scored is {self.runs}')
    print(f'Is the player out ? : {self.isOut}')
    print(f'probability of getting out: {self.pOutList}')
    print(f'probability of scoring runs: {self.pRun}')
    print(f'The number of balls played by this player is {self.balls_played_by_thisPlayer}')


class ODI:
  
  def __init__(self) -> None:
    self.ballsPlayed = 0
    self.ballsLeft = 300
    self.totalRuns = 0
    self.players = [Player(i+1) for i in range(10)]
    # list of player
    self.isActive = True
    self.currentPlayerIndex = 1
    # first player will be player 1
    self.currentPlayerObject = self.players[self.currentPlayerIndex - 1]
    # player object of the current player

    self.wicketsTaken = 0
    self.wicketsInHand = 10
    self.currentState = (self.ballsLeft,self.wicketsInHand)


  def print_state_of_odi(self):
    print(f'The number of balls played and balls remaining is {self.ballsPlayed} and {self.ballsLeft} respectively')
    print(f'Total Runs: {self.totalRuns}')
    print(f'The current player index is {self.currentPlayerIndex}')
    print(f'the current player is {self.currentPlayerObject.player_tuple}')
    print(f'wickets taken: {self.wicketsTaken}')
    print(f'wickets in hand: {self.wicketsInHand}')
    print(f'the current state of odi: {self.currentState}')

  def ballPlayed(self,whoPlayedTheBall: Player,runs_scored = 0,is_wicket = False):
    # whoPlayedTheBall is a player object
    if self.ballsPlayed == 300:
      odi.isActive = False
      return
    
    self.ballsPlayed += 1
    self.ballsLeft -= 1
    whoPlayedTheBall.balls_played_by_thisPlayer+=1

    if is_wicket:
      # if wicket happens
      self.wicketsTaken += 1
      self.wicketsInHand -= 1
      # what if current player index crosses 10
      if self.currentPlayerIndex == 10:
        odi.isActive = False
        return
      self.currentPlayerIndex += 1
      self.currentPlayerObject = self.players[self.currentPlayerIndex - 1]
      whoPlayedTheBall.isOut = True
      self.currentState = (self.ballsLeft,self.wicketsInHand)


    else:
      whoPlayedTheBall.runs += runs_scored
      self.totalRuns += runs_scored


# 3a
def playBall(odi: ODI,a_t = 0) -> tuple:
  a_t = int(input()) if a_t == 0 else a_t
  if a_t == 5:
    print('no such run')
    return (0,odi.currentState)
  playerObject = odi.currentPlayerObject
  indexOfShot = playerObject.shots.index(a_t)
  # print(indexOfShot)
  
  pOutList  = playerObject.pOutList
  # pRun = playerObject.pRun
  # print(pOutList)
  isOut = rnd.choices(
    [True,False], 
    weights=[pOutList[indexOfShot],1-pOutList[indexOfShot]],
    k=1
  )[0]
  if isOut:
    odi.ballPlayed(playerObject,is_wicket=True)
    return (0,odi.currentState)
  else:
    pRun = playerObject.pRun
    doesScoreRun = rnd.choices(
      [True,False],
      weights=[pRun,1-pRun],
      k=1
    )[0]
    if not doesScoreRun:
      # dot ball
      odi.ballPlayed(playerObject)
      return (0,odi.currentState)
    else:
      runsScored = a_t
      odi.ballPlayed(playerObject,runs_scored=runsScored)
      return (runsScored,odi.currentState)

odi = ODI()
# odi.print_state_of_odi()
# playBall(odi)
# odi.print_state_of_odi()

i = 0
odi.print_state_of_odi()
while i<300 and odi.isActive:
  playBall(
    odi,
    a_t=rnd.choices([1,2,3,4,6],k=1)[0]
  )
  print(odi.currentState, odi.totalRuns)
  i+=1
  




