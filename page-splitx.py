# extend a connected component in the middle by drawing a line extending out
# from its centre (or maybe centre of gravity)

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

sects = onebit.splitx_left()

i = 0
for se in sects:
  se.save_PNG("./results/"+bname+str(i)+".png")
  i = i + 1

sects = onebit.splitx_right()

for se in sects:
  se.save_PNG("./results/"+bname+str(i)+".png")
  i = i + 1

