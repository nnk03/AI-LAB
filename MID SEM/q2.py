import random as rnd

def generatePoint(m: int, n:int):
  x = m + rnd.random()*abs(n-m)
  y = m + rnd.random()*abs(n-m)
  return x,y

# estimate area of parabola under the curve y = x squared

z = int(1e6)

num_points_under_parabola = 0
for _ in range(z):
  x,y = generatePoint(0,1)
  if y < x*x:
    num_points_under_parabola += 1

area_of_parabola = num_points_under_parabola / z

print('The area of the region under the parabola y = x^2 where x is from 0 to 1 is')
print(area_of_parabola)


num_points_inside_circle = 0
for _ in range(z):
  x,y = generatePoint(0,1)
  if (x-0.5)**2 + (y-0.5)**2 <= 0.25:
    num_points_inside_circle += 1

area_of_circle = num_points_inside_circle / z

pi_approx = 4 * area_of_circle
print(f'The approximate value of pi is {pi_approx}')




