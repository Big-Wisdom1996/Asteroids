from math import *

radius = [15,15,9,15,15,12,15,15,9]
angle =  [0,1/3,2/3,3/4,7/6,5/4,8/6,7/4,7/4]

x = []
y = []

for i in range(0,len(radius)):
    x.append(round(radius[i]*cos(angle[i]*pi),0))
    y.append(round(radius[i]*sin(angle[i]*pi),0))

print(x)
print(y)

coords = []

for i in range(0,len(x)):
    coords.append((x[i],y[i]))

#print(coords)
