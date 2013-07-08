# just to test, pick a random connected component and save an image where only
# it and its neighbours within a certain distance are displayed

from gamera.core import *
import sys
import string
import os.path
import time
import os
import math
import random

init_gamera()

bname = os.path.basename(sys.argv[1])
if '.' in bname:
  bname = string.join(bname.split('.')[0:-1],'.')
else:
  bname = bname

img = load_image(sys.argv[1])

onebit = img.djvu_threshold()

ccs = onebit.cc_analysis()

cc = random.choice(ccs)
ccmoms = cc.moments()
cccenter = (cc.offset_x + cc.ncols*ccmoms[0], cc.offset_y + cc.nrows*ccmoms[1])

# the threshold distance
rad = float(sys.argv[2])

def dist_func(x):
  pdists = cc.polar_distance(x)
  print pdists[0]
  return pdists[0] < rad

closeccs = filter(dist_func, ccs)

print len(closeccs)

blank = Image(img.ul, img.lr, ONEBIT)

for c in closeccs:
  blank.highlight(c,1)

savpath = "./results/close_ccs"+time.strftime("%y-%m-%d_%H_%M_%S")+".png"
blank.save_PNG(savpath)



