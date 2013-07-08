# print the resulting labelling from the cc analysis algorithm

from gamera.core import *
import sys
from connection_functions import *
import random
from gamera import graph
from gamera import graph_util

init_gamera()

img = load_image(sys.argv[1]).to_onebit()

ccimg = Image(img.ul, img.lr)

ccs = img.cc_analysis()
for cc in ccs:
  ccimg.highlight(cc, cc.label)

g = make_horizontal_cc_graph(img,ccs)
for e in sorted(g.get_edges(), key=lambda x: x.from_node):
  print e

print "Length: ", len(g.get_edges())

print dir(e)
