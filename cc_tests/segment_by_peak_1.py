# finds the maxima using peakdetect, then splits the image into subimages
# acccording to the valleys between these peaks

from gamera.core import *
import sys
from connection_functions import *
from peakdetect import *
import random
from gamera import graph
from gamera import graph_util
import os.path
import time

init_gamera()

rgbimg = load_image(sys.argv[1]).to_rgb()
img = rgbimg.to_onebit()

# The horizontal projection of the image
hp = img.projection_rows()

# find peaks in the horizontal projection
maxtab, mintab = peakdet(hp,delta=10,minimum_y_threshold=500)

print maxtab

# the y values of the projection peaks
peaksy = sorted([m[0] for m in maxtab] + [img.lr.y])

n = len(peaksy) - 1

# find the y values limiting the image splits
ysplitpairs = zip([0]+[(peaksy[i] + peaksy[i-1])/2.0 for i in \
    xrange(1,n)],[(peaksy[i] + peaksy[i-1])/2.0 for i in xrange(1,n+1)])

print ysplitpairs

i = 0
# split the image up into subimages
for y0, y1 in ysplitpairs:
  print "Splitting image at coordinates: ", (0,y0), (rgbimg.lr.x,y1)
  subimg = rgbimg.subimage((0,y0),(rgbimg.lr.x,y1))
  pathprepend = sys.argv[2]
  imgpath = pathprepend+"/subimg_"+str(i)+"_"+time.strftime("%y-%m-%d_%H_%M_%S")\
    +"-"+os.path.basename(sys.argv[1])
  print "Saving to: ", imgpath
  subimg.save_PNG(imgpath)
  i = i + 1
