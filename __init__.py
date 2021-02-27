from math import cos, sin, exp
from root import *

f = lambda x: x**2 - 4*cos(x)

m = Descartes(f, 1, 1.3)
m.compute()
print (m)