from connection_functions import *

from gamera.core import *
import sys
import random
import time

init_gamera()

img = load_image(sys.argv[1])

nameidx = sys.argv[2]

radthresh = float(sys.argv[3])

onebit = img.to_onebit()

ccs = onebit.cc_analysis()

random.seed()

a = random.choice(ccs)

for b in ccs:
  if a.polar_distance(b)[0] < radthresh:
    try:
      x0,y0,x1,y1 = shortest_horizontal_bridge(a,b)
    except StandardError:
      continue
    onebit.draw_line((x0,y0),(x1,y1),1)

savdir = \
"./results/ccs_bridges_"+time.strftime("%y-%m-%d_%H_%M_%S")+"-"+str(nameidx)

onebit.save_PNG(savdir+".png")
