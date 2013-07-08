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

hullimg = scoremask.convex_hull_as_image()
points = scoremask.convex_hull_as_points()
print points
minx = int((min(points, key=lambda p: p.x)).x+img.ncols*(float(sys.argv[3])))
print minx
miny = int((min(points, key=lambda p: p.y)).y+img.nrows*(float(sys.argv[4])))
print miny
maxx = int((max(points, key=lambda p: p.x)).x-img.ncols*(float(sys.argv[5])))
print maxx
maxy = int((max(points, key=lambda p: p.y)).y-img.nrows*(float(sys.argv[6])))
print maxy

maskedimg.draw_hollow_rect(Point(minx,miny),Point(maxx,maxy),RGBPixel(255,0,0))
croppedimg = img.subimage(Point(minx,miny),Point(maxx,maxy))


# save the masked image
pathprepend = sys.argv[2]
maskpath = pathprepend+"/mask_"+time.strftime("%y-%m-%d_%H_%M_%S")\
  +"-"+os.path.basename(sys.argv[1])
imgpath = pathprepend+"/hl_"+time.strftime("%y-%m-%d_%H_%M_%S")\
  +"-"+os.path.basename(sys.argv[1])
hullpath = pathprepend+"/hull_"+time.strftime("%y-%m-%d_%H_%M_%S")\
  +"-"+os.path.basename(sys.argv[1])
croppedpath = pathprepend+"/cropped_"+time.strftime("%y-%m-%d_%H_%M_%S")\
  +"-"+os.path.basename(sys.argv[1])

print "Saving to: ", croppedpath
croppedimg.save_PNG(croppedpath)
#scoremask.save_PNG(maskpath)
#hullimg.save_PNG(hullpath)
