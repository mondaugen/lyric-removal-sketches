# trying out the polynomials in scipy
# fit a polynomial of specified order in least-squares sense
# this works poorly

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy import signal
import sys
from peakdetect import *

y = []
for line in sys.stdin:
  y.append(float(line))

x = np.arange(0,len(y))

maxtab, mintab = peakdet(y,delta=10, minimum_y_threshold=500)
plt.plot(y)
print maxtab
plt.scatter(array(maxtab)[:,0], array(maxtab)[:,1], color='blue')
# plt.scatter(array(mintab)[:,0], array(mintab)[:,1], color='red')
plt.show()
