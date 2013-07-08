# find the horizontal projections of half sides of an image

from gamera.core import *
import sys
import time
import os
from peakdetect import *

init_gamera()

rgbimg = load_image(sys.argv[1]).to_rgb()

img = rgbimg.to_onebit()

# split the image into two subimages

image_split_l = img.subimage(Point(img.ul_x,img.ul_y), Size(img.width / 2, img.height))
image_split_r = img.subimage(Point(img.ul_x + img.width / 2, img.ul_y), Size(img.width / 2, \
  img.height))

hp_left = image_split_l.projection_rows()
hp_right = image_split_r.projection_rows()

leftmaxtab, leftmintab = peakdet(hp_left,delta=10,minimum_y_threshold=100)
rightmaxtab, rightmintab = peakdet(hp_right,delta=10,minimum_y_threshold=100)

leftpeaksy = sorted([m[0] for m in leftmaxtab])
rightpeaksy = sorted([m[0] for m in rightmaxtab])

print 'Left y coords of peaks', str(leftpeaksy)
print 'Right y coords of peaks', str(rightpeaksy)

for y0, y1 in zip(leftpeaksy, rightpeaksy):
  rgbimg.draw_line(Point(rgbimg.ul.x, y0), Point(rgbimg.lr.x, y1), \
  RGBPixel(255,0,0))

pathprepend = sys.argv[2]
imagepath = pathprepend + "/lr_line_" + time.strftime("%y-%m-%d_%H_%M_%S")\
    +"-"+os.path.basename(sys.argv[1])
print "Saving to: ", imagepath

rgbimg.save_PNG( imagepath )
