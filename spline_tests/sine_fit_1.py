# trying out the polynomials in scipy
# fit a polynomial of specified order in least-squares sense
# this works poorly

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from scipy import interpolate
import math
import sys

y = []
for line in sys.stdin:
  y.append(float(line))

x = np.arange(0,len(y))

# fill a matrix with argv[2] sines of frequency argv[1]
# fills with argv[2] phase offsets

a = []
nphs = int(sys.argv[2])
freq = float(sys.argv[1]) + 0.5
n = float(len(y))

for i in xrange(nphs):
  a.append([math.sin(math.pi*2*(freq * (float(j)/n) \
    + float(i)/float(nphs))) for j in xrange(int(n))])

a = np.array(a)
#print a
A = np.asmatrix(a.transpose())
print A
sol, g1, g2, g3 = np.linalg.lstsq(A, y)
maxidx = np.argmax(sol)
newsol = np.matlib.zeros((len(sol),1))
newsol[maxidx][0] = 1
sol = np.asmatrix(sol)
print sol
yest = A * newsol
plt.figure()
plt.plot(x,y,'b-')
plt.plot(x,yest,'g-')
plt.show()
