# print the resulting labelling from the cc analysis algorithm
# the start and end points are given as x0 y0 x1 y1 pairs through stdin

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

ccimg = Image(img.ul, img.lr)

ccs = img.cc_analysis()
for cc in ccs:
  ccimg.highlight(cc, cc.label)

# The horizontal projection of the image
hp = img.projection_rows()

# find peaks in the horizontal projection
maxtab, mintab = peakdet(hp,delta=10,minimum_y_threshold=500)

for cc in ccs:
  print "id: ", cc.label, "ul: ", cc.ul.x, cc.ul.y, "lr: ", cc.lr.x, cc.lr.y

start_x = 0
start_y = 0
  
g = make_horizontal_cc_graph(img,ccs)

def y_in_cc_box_range(cc):
  # returns true if start_y is between cc.ul.y and cc.lr.y
  return ((cc.ul.y <= start_y) and (start_y <= cc.lr.y))

def start_point_in_cc_box(cc):
  result = (cc.ul.x <= start_x)
  result = result and (cc.ul.y <= start_y)
  result = result and (start_x <= cc.lr.x)
  result = result and (start_y <= cc.lr.y)
  return result

def end_point_in_cc_box(cc):
  result = ((cc.ul.x <= end_x) & (cc.ul.y <= end_y)\
    & (end_x <= cc.lr.x) & (end_y <= cc.lr.y))
  return result

for x,y in maxtab:

  # the coordinates of the start component
  start_y = int(x)

  # the coordinates of the end component
  end_y = int(x)

  # find ccs that enclose the y coordinate and sort by ul-x-coordinate
  rowccs = sorted(filter(y_in_cc_box_range,ccs), key=lambda cc: cc.ul.x)

  try:
    start_cc = rowccs[0]
  except IndexError:
    sys.stderr.write("No start component at peak %f\n" % (starty,))
    continue
  try:
    end_cc = rowccs[-1]
  except IndexError:
    sys.stderr.write("No end component at peak %f\n" % (endy,))
    continue

  print "Start: ", start_cc.ul.x, start_cc.ul.y
  print "End: ", end_cc.ul.x, end_cc.ul.y
  
  
  paths = g.dijkstra_all_pairs_shortest_path()
  print "Path from ", start_cc.label, "to ", end_cc.label, ": ",\
      paths[start_cc.label][end_cc.label]
  
  dist, pathcclabels = paths[start_cc.label][end_cc.label]
  pathccs = filter(lambda x: x.label in pathcclabels, ccs)
  
  for p in pathccs:
    rgbimg.highlight(p, RGBPixel(255,0,0))

pathprepend = sys.argv[2]
imgpath = pathprepend+"/hl_"+time.strftime("%y-%m-%d_%H_%M_%S")\
    +"-"+os.path.basename(sys.argv[1])
print "Saving to: ", imgpath

rgbimg.save_PNG(imgpath)
