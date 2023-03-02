# 
import queue
import random as rnd
import sys

q = queue.PriorityQueue()
qlist = list(range(10))
rnd.shuffle(qlist)

print(qlist)
for x in qlist:
  q.put((x,x))

for x in list(q.queue):
  print(x,end=' ')

class CustomClass:
  def __init__(self,x,toCompare=0) -> None:
    self.integer = x
    self.toCompare = toCompare
  
  # def __lt__(self,other):
  #   return self.toCompare < other.toCompare 



print()
qlistObjects = [
  CustomClass(x) for x in [1,1,1,]
]



# print(qlistObjects)
# q2 = queue.PriorityQueue()
# for x in qlistObjects:
#   q2.put((x.integer,x))

# for data in list(q2.queue):
#   print(data)

print(sys.getsizeof(qlistObjects[0]))
