lst = list(map(int, input().split()))
n = len(lst)
dp = [0 for _ in range(n+1)]
dp[0] = 0
for i in range(1, n+1):
  dp[i] = min([
    dp[j] + (200 - ((-lst[j] if j!=0 else 0) + lst[i-1]))**2 for j in range(i)
  ])

print(dp[-1])