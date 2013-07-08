# print the resulting labelling from the cc analysis algorithm

from gamera.core import *
import sys
from connection_functions import *
import random
from gamera import graph
from gamera import graph_util

init_gamera()

img = load_image(sys.argv[1])

ccimg = Image(img.ul, img.lr)

ccs = img.cc_analysis()
for cc in ccs:
  ccimg.highlight(cc, cc.label)

for j in xrange(ccimg.height):
  for i in xrange(ccimg.width):
    sys.stdout.write(('%1c' % (33 + ccimg.get((i,j)))))
  print

g = make_horizontal_cc_graph(img,ccs)

paths = g.dijkstra_all_pairs_shortest_path()
for k in paths.keys():
  print k, paths[k]

