# print the resulting labelling from the cc analysis algorithm

from gamera.core import *
import sys
from connection_functions import *
import random

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

cc = random.choice(ccs)
for node in g.BFS(cc.label):
  print node(),
