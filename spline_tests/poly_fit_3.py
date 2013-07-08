# trying out the polynomials in scipy
# fit a polynomial of specified order in least-squares sense
# this works poorly

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import sys

y = []
for line in sys.stdin:
  y.append(float(line))

x = np.arange(0,len(y))

tck = interpolate.splrep(x,y)
ytck = interpolate.splev(tck,x)

plt.figure()
plt.plot(x,y,'x',x,ypoly,'-g')
plt.show()
