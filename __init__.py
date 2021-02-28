from math import cos, sin, exp
from root import *

f = lambda x: 1+7/x

m = Newton(f, lambda x: -7/x**2, -8, tolerance = 1e-9)
m.compute()
print (m)
print (m.progression)