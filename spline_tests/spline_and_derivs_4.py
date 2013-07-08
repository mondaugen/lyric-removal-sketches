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

t = np.arange(0,1.1,.1)
x = np.sin(2*np.pi*t)
y = np.cos(2*np.pi*t)
tck,u = interpolate.splprep([x,y],s=0)
unew = np.arange(0,1.01,0.01)
out = interpolate.splev(unew,tck)
plt.figure()
plt.plot(x,y,'x',out[0],out[1],np.sin(2*np.pi*unew),np.cos(2*np.pi*unew),x,y,'b')
plt.legend(['Linear','Cubic Spline', 'True'])
plt.axis([-1.05,1.05,-1.05,1.05])
plt.title('Spline of parametrically-defined curve')
plt.show()
