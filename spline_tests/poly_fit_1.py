# trying out the polynomials in scipy

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import sys

y = []
for line in sys.stdin:
  y.append(float(line))

x = np.arange(0,len(y))
plt.figure()
plt.plot(x,y,'x')
plt.show()
