import math as math
import matplotlib as plt
import numpy as np

p = np.poly1d([1, 2, 10, -2])
err = 0.5 * math.pow(10, -5)
z = 2
a3 = p[3]
bi = 0
ci = 0
diff = 5
estimates = [2]

count = 0
while abs(diff) > err or count == 10:
    count+1
    #horners method to get f(x), f'(x) given root of z.
    for i in reversed(range(4)):
       b = p[i] + (z*bi)
       bi = b
       if (i > 0): #Stop calculating at c1
           c = b + (z*ci)
           ci = c
       print("z = ", z, " i = ", i, " b = ", b, " c = ", c, " count = " ,count)

    z = z - (b / c) #root = p - f(p) / f'(p). Core of newton's method
    estimates.append(z) #add the root to list
    diff = (estimates[len(estimates)-1] - estimates[len(estimates)-2])
    print("z: ", z, " diff: ", diff)

counts = [1,2,3,4,5,6,7,8,9,10]
plt.plot(counts, estimates)
    

