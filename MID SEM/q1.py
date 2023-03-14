import random as rnd
import matplotlib.pyplot as plt

def montyHall(n: int):
  isGift = [0 for _ in range(n)]
  giftIndex = rnd.randrange(0,n)
  firstChoice = rnd.randrange(0,n)
  # assuming monty opened all boxes which are neither gift box or the box which the player chose
  montyOpenedDoors = [
    i for i in range(n) if i!=giftIndex and i!=firstChoice
  ]
  if firstChoice == giftIndex:
    # if switching leads to losing the gift, we return False
    return False
  else:
    return True
  
def probability_win(n: int):
  count_wins = 0
  for _ in range(1000):
    if montyHall(n):
      count_wins += 1
  
  return count_wins / 1000


n_value = [ i for i in range(3,101)]
probabilty_n = [
  probability_win(i) for i in range(3,101)
]

plt.xlabel('VALUE OF N')
plt.ylabel('PROBABILITY OF WINNING IF SWITCHED')
plt.title('Probablity of winning vs values for n')
plt.bar(n_value,probabilty_n)
plt.show()