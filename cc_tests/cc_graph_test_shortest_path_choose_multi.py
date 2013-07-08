# print the resulting labelling from the cc analysis algorithm
# the start and end points are given as x0 y0 x1 y1 pairs through stdin

from gamera.core import *
import sys
from connection_functions import *
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

#for j in xrange(ccimg.height):
#  for i in xrange(ccimg.width):
#    sys.stdout.write(('%1c' % (33 + ccimg.get((i,j)))))
#print


start_x = 0
start_y = 0
end_x = 0
end_y = 0

for cc in ccs:
  print "id: ", cc.label, "ul: ", cc.ul.x, cc.ul.y, "lr: ", cc.lr.x, cc.lr.y

print

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

for line in sys.stdin:
  args = line.split()

  # the coordinates of the start component
  start_x = int(args[0])
  start_y = int(args[1])

  # the coordinates of the end component
  end_x = int(args[2])
  end_y = int(args[3])

  print "Start: ", start_x, start_y
  print "End: ",end_x, end_y
  
  # arbitrarily choose the first if there are more than one for which the
  # functions are true (this shouldn't change what path be found)
  try:
    start_cc = (filter(start_point_in_cc_box, ccs))[0]
  except IndexError:
    sys.stderr.write("No component under start point\n")
    continue
  try:
    end_cc = (filter(end_point_in_cc_box, ccs))[0]
  except IndexError:
    sys.stderr.write("No component under end point\n")
    continue
  
  g = make_horizontal_cc_graph(img,ccs)
  
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
