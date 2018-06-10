import numpy
from math import *

A = numpy.array([
    [3],
    [4]])
    

B = numpy.array([
    [1,2],
    [3,4]])

B[0][0] = 0
eli = (B * A)
    
print(eli)
