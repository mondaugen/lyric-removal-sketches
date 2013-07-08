# find the horizontal projections of half sides of an image

from gamera.core import *
import sys
import time
import os

init_gamera()

rgbimg = load_image(sys.argv[1]).to_rgb()

img = rgbimg.to_onebit()

# split the image into two subimages

image_split_l = img.subimage(Point(img.ul_x,img.ul_y), Size(img.width / 2, img.height))
image_split_r = img.subimage(Point(img.ul_x + img.width / 2, img.ul_y), Size(img.width / 2, \
  img.height))

pathprepend = sys.argv[2]
leftimagepath = pathprepend + "/left_" + time.strftime("%y-%m-%d_%H_%M_%S")\
    +"-"+os.path.basename(sys.argv[1])
rightimagepath = pathprepend + "/right_" + time.strftime("%y-%m-%d_%H_%M_%S")\
    +"-"+os.path.basename(sys.argv[1])
print "Saving to: ", leftimagepath, "and", rightimagepath

image_split_l.save_PNG(leftimagepath)
image_split_r.save_PNG(rightimagepath)
