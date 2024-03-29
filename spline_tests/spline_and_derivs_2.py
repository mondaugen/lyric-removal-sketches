# trying out the splines in scipy

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# cubic spline
x = np.arange(0,2*np.pi+np.pi/4,2*np.pi/8)
y = np.sin(x)
tck = interpolate.splrep(x,y,s=0)
xnew = np.arange(0,2*np.pi,np.pi/50)
ynew = interpolate.splev(xnew,tck,der=0)

yder = interpolate.splev(xnew,tck,der=1)
plt.figure()
plt.plot(xnew,yder,xnew,np.cos(xnew),'--')
plt.legend(['Cubic Spline', 'True'])
plt.axis([-0.05,6.33,-1.05,1.05])
plt.title('Derivative estimation from spline')
plt.show()
