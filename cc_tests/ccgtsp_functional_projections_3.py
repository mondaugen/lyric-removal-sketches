# find the projections of image beneath a function of a line
# the starting points use peaks in the horizontal projection
# the lines are generated as rotations around a midpoint along the length of the
# image, rather than a left point

from gamera.core import *
import sys
import time
import os
from peakdetect import *
import math

# arg 1 is source file
# arg 2 is destination folder
# arg 3 is the minimum y threshold
# arg 4 is the number of searches to do at each height division
# arg 5-6 are the negative and positive height bounds around which to search
# example: ./source_file ./dest_dir 10 4 10 10
# will do 10 * 4 = 40 searches, each line starting from h_i = height/10 * (i + 0.5) for i
# in [0,10) and searching to end_h_j = (h_i) - 10 + (10 + 10)* (j + 0.5) / 4 for
# j in [0,4)

def count_colour_under_function(image, func, colour=0):
  count = 0
  for x in xrange(image.ul.x, image.lr.x):
    if image.get((x,round(func(x)))) == colour:
      count = count + 1
  return count

def linear_equation_from_points(p0, p1):
  x0, y0 = p0
  x1, y1 = p1
  def _lin_func(x):
    return float(y1 - y0)/float(x1 - x0) * (x - x0) + y0
  return _lin_func

init_gamera()

rgbimg = load_image(sys.argv[1]).to_rgb()

img = rgbimg.to_onebit()

# The horizontal projection of the image
hp = img.projection_rows()

# find peaks in the horizontal projection
maxtab, mintab = peakdet(hp,delta=10,minimum_y_threshold=float(sys.argv[3]))

# the y values of the projection peaks
peaksy = sorted([m[0] for m in maxtab] + [img.lr.y])

numdivs     = len(peaksy)
numsearches = float(sys.argv[4])
negbound    = float(sys.argv[5])
posbound    = float(sys.argv[6])

blackest_lines = []

for ys in peaksy:
  y_ends = [ ys - negbound + (posbound + negbound) * (float(i) + 0.5) \
      / numsearches for i in xrange(int(numsearches)) ]
  # filter out y_ends that are above the upper right corner or below the lower
  # left
  y_ends = filter(lambda item: ((item > img.ur.y) and (item < img.lr.y)), y_ends)
#  print 'ur.y', img.ur.y, 'lr.y', img.lr.y
#  print 'y_ends', y_ends
  black_counts = [ count_colour_under_function(img, \
      linear_equation_from_points((img.ul.x, yl), (img.ur.x, yr))) \
      for yl, yr in zip(reversed(y_ends), y_ends) ]
  # line is returned as array of two points, [(x0,y0),(x1,y1)]
  blackest_lines.append([(img.ul.x, \
    y_ends[ len(y_ends) - black_counts.index(min(black_counts)) - 1 ]), \
    (img.lr.x, y_ends[ black_counts.index(min(black_counts)) ])])

for p0, p1 in blackest_lines:
  rgbimg.draw_line(p0, p1, RGBPixel(255, 0, 0))

pathprepend = sys.argv[2]
imagepath = pathprepend + "/lr_line_" + time.strftime("%y-%m-%d_%H_%M_%S")\
    +"-"+os.path.basename(sys.argv[1])
print "Saving to: ", imagepath

rgbimg.save_PNG( imagepath )
