# trying out the splines in scipy

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# cubic spline
y = np.array([1,0.5,2,0.75,3,0.3,4,-0.6])
x = np.array([0,1,2,3,4,5,6,6.5])
tck = interpolate.splrep(x,y,k=3,s=0)
print tck
xnew = np.arange(0,len(y),0.1)
ynew = interpolate.splev(xnew,tck,der=0)

dtck = interpolate.splrep(xnew,ynew,s=0)

print interpolate.sproot(dtck)

plt.figure()
plt.plot(x,y,'x',xnew,ynew,'g-')
plt.legend(['Linear','Cubic Spline'])
#plt.axis([-0.05,6.33,-1.05,1.05])
plt.title('Cubic-spline interpolation')
plt.show()
