# extend a connected component in the middle by drawing a line extending out
# from its centre. The length of line line is relative to the weight of the
# connected component (how many black pixels)

from gamera.core import *
import sys
import string
import os.path

init_gamera()

bname = os.path.basename(sys.argv[1])
if '.' in bname:
  bname = string.join(bname.split('.')[0:-1],'.')
else:
  bname = bname

img = load_image(sys.argv[1])

onebit = img.djvu_threshold()

ccs = onebit.cc_analysis()

# draw a line extending out horizontally from the centre of all connected components

weightc = float(sys.argv[2])

for c in ccs:
  ex = int(weightc * float(c.black_area()[0]))
  centrex = c.offset_x + float(c.ncols) / 2.
  centrey = c.offset_y + float(c.nrows) / 2.
  lstartx = c.offset_x - ex
  lstarty = centrey
  lendx = c.offset_x + ex
  lendy = centrey
  # check to see that the end points of the line do not go off the canvas
  if lstartx < 0:
    lstartx = 0
  if lendx >= onebit.offset_x + onebit.ncols:
    lendx = onebit.offset_x + onebit.ncols - 1
  onebit.draw_line((lstartx,lstarty), (lendx, lendy), c.label, 2)

onebit.save_PNG("./results/"+bname+"_w_weight_lines"+str(weightc)+".png")


