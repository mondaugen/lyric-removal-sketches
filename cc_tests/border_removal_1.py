# how do we remove borders

from gamera.core import *
from gamera.toolkits import border_removal
import sys
import time
import os.path

init_gamera()

img = load_image(sys.argv[1])

gryimg = img.to_greyscale()

scoremask = gryimg.border_removal(win_dil=3, threshold1_gradient=6.0, \
    threshold2_gradient=6.0, threshold1_scale=0.8, threshold2_scale=0.8)

maskedimg = img.mask(scoremask)

# save the masked image
pathprepend = sys.argv[2]
maskpath = pathprepend+"/mask_"+time.strftime("%y-%m-%d_%H_%M_%S")\
  +"-"+os.path.basename(sys.argv[1])
imgpath = pathprepend+"/hl_"+time.strftime("%y-%m-%d_%H_%M_%S")\
  +"-"+os.path.basename(sys.argv[1])
print "Saving to: ", imgpath
maskedimg.save_PNG(imgpath)
scoremask.save_PNG(maskpath)
