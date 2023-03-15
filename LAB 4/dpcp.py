import copy

mylst = [
  [1,2,3],
  [2,3,4,],
  [5,6,7]

]
mylst2 = copy.deepcopy(mylst)
mylst3 = copy.copy(mylst)

print(mylst)
print(mylst2)
print(mylst3)
mylst2[1][2] = 100
print(mylst[1][2])
print(mylst2[1][2])

mylst3[1][2] = 10000000
print(mylst[1][2])
print(mylst3[1][2])
print(mylst)
print(mylst2)
print(mylst3)