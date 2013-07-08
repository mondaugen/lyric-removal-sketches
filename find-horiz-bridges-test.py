from connection_functions import *

from gamera.core import *
import sys
import random
import time

init_gamera()

# Only use this on an image you know has two ccs

img = load_image(sys.argv[1])

nameidx = sys.argv[2]

onebit = img.to_onebit()

ccs = onebit.cc_analysis()

random.seed()

a = random.choice(ccs)

for b in ccs:
  try:
    x0,y0,x1,y1 = shortest_horizontal_bridge(a,b)
  except StandardError:
    continue
  onebit.draw_line((x0,y0),(x1,y1),1)

savdir = \
"./results/ccs_bridges_"+time.strftime("%y-%m-%d_%H_%M_%S")+"-"+str(nameidx)

onebit.save_PNG(savdir+".png")
