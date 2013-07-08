# trying out the splines in scipy

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# cubic spline
y = np.array([1,0.5,2,0.75,3,0.3])
x = np.arange(0,len(y),1)

tck = interpolate.splrep(x,y,s=0)
xnew = np.arange(0,len(y),0.25)
ynew = interpolate.splev(xnew,tck,der=1)

plt.figure()
plt.plot(x,y,'x',xnew,ynew,'g-')
plt.legend(['Linear','Cubic Spline'])
#plt.axis([-0.05,6.33,-1.05,1.05])
plt.title('Cubic-spline interpolation')
plt.show()
