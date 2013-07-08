# print the resulting labelling from the cc analysis algorithm

from gamera.core import *
import sys
from connection_functions import *
from peakdetect import *
import random
from gamera import graph
from gamera import graph_util
import os.path

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

#for j in xrange(ccimg.height):
#  for i in xrange(ccimg.width):
#    sys.stdout.write(('%1c' % (33 + ccimg.get((i,j)))))
#print


# the coordinates of the start component
start_x = int(sys.argv[2])
start_y = int(sys.argv[3])
# the coordinates of the end component
end_x = int(sys.argv[4])
end_y = int(sys.argv[5])

print "Start: ", start_x, start_y
print "End: ",end_x, end_y

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

# arbitrarily choose the first if there are more than one for which the
# functions are true
start_cc = (filter(start_point_in_cc_box, ccs))[0]
end_cc = (filter(end_point_in_cc_box, ccs))[0]

g = make_horizontal_cc_graph(img,ccs)

paths = g.dijkstra_all_pairs_shortest_path()
print "Path from ", start_cc.label, "to ", end_cc.label, ": ",\
    paths[start_cc.label][end_cc.label]

dist, pathcclabels = paths[start_cc.label][end_cc.label]
pathccs = filter(lambda x: x.label in pathcclabels, ccs)

for p in pathccs:
  rgbimg.highlight(p, RGBPixel(255,0,0))

rgbimg.save_PNG("hl_"+os.path.basename(sys.argv[1]))

