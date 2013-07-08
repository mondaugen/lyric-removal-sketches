# print the resulting labelling from the cc analysis algorithm
# finds the maxima using peakdetect, then splits the image into subimages
# acccording to the valleys between these peaks, then looks for paths in the sub
# image
# the search algorithm here will timeout if taking too long to find a path

from gamera.core import *
import sys
from connection_functions import *
from peakdetect import *
import random
from gamera import graph
from gamera import graph_util
import os.path
import time
import thread
import threading

# only wait this long (in seconds) before interrupting the thread
#SEARCH_WAIT_TIME = float(sys.argv[3])

init_gamera()

rgbimg = load_image(sys.argv[1]).to_rgb()
img = rgbimg.to_onebit()

# The horizontal projection of the image
hp = img.projection_rows()

# find peaks in the horizontal projection
maxtab, mintab = peakdet(hp,delta=10,minimum_y_threshold=500)

# the y values of the projection peaks
peaksy = sorted([m[0] for m in maxtab] + [img.lr.y])

n = len(peaksy) - 1

# find the y values limiting the image splits
ysplitpairs = zip([0]+[(peaksy[i] + peaksy[i-1])/2.0 for i in \
    xrange(1,n)],[(peaksy[i] + peaksy[i-1])/2.0 for i in xrange(1,n+1)])

print ysplitpairs


start_x = 0
start_y = 0

def y_in_cc_box_range(cc):
  # returns true if start_y is between cc.ul.y and cc.lr.y
  return ((cc.ul.y <= start_y) and (start_y <= cc.lr.y))

def start_point_in_cc_box(cc):
  result = (cc.ul.x <= start_x)
  result = result and (cc.ul.y <= start_y)
  result = result and (start_x <= cc.lr.x)
  result = result and (start_y <= cc.lr.y)
  return result

def end_point_in_cc_box(cc):
  result = ((cc.ul.x <= end_x) & (cc.ul.y <= end_y)\
    & (end_x <= cc.lr.x) & (end_y <= cc.lr.y))
  return result

# do connected component analysis on the image
ccs = img.cc_analysis()

for i in xrange(len(maxtab)):
  x, y = maxtab[i]

  # make a sub image just viewing a horizontal slice of the image
  subimg = img.subimage(Point(img.ul.x,int(ysplitpairs[i][0])), \
      Point(img.lr.x, int(ysplitpairs[i][1])))
  
  # make an empty image with the height of the limiting y values found from the peaks
  subimg = subimg.image_copy()

  #ccimg.fill(0)

  # find the ccs in the subimage
  subccs = subimg.cc_analysis()

  # highlight the new image with ccs
  for j in xrange(len(subccs)):
    # do bounds check
  #  if ((cc.ul.x >= ccimg.ul.x) and (cc.ul.y >= ccimg.ul.y) \
  #      and (cc.lr.x <= ccimg.lr.x) and (cc.lr.y <= ccimg.lr.y)):
  #    ccimg.highlight(cc, cc.label)
      print "id: ", subccs[j].label, "ul: ", subccs[j].ul.x, subccs[j].ul.y, \
          "lr: ", subccs[j].lr.x, subccs[j].lr.y, "Y offset:", \
          subccs[j].offset_y
      subccs[j].ul.y = subccs[j].ul.y - int(ysplitpairs[i][0])
      subccs[j].lr.y = subccs[j].lr.y - int(ysplitpairs[i][0])
      print "id: ", subccs[j].label, "ul: ", subccs[j].ul.x, subccs[j].ul.y, \
          "lr: ", subccs[j].lr.x, subccs[j].lr.y, "Y offset:", \
          subccs[j].offset_y

  print "Y Offset: %d" % (int(ysplitpairs[i][0]),)
  print "subimg Y offset: %d" % (subimg.offset_y,)

  # make a graph of ccs on the subimage
  g = make_horizontal_cc_graph(subimg,subccs)

  # the coordinates of the start component
  start_y = int(x)

  # the coordinates of the end component
  end_y = int(x)

  # find ccs that enclose the y coordinate and sort by ul-x-coordinate
  rowccs = sorted(filter(y_in_cc_box_range,subccs), key=lambda cc: cc.ul.x)

  print rowccs

  try:
    start_cc = rowccs[0]
  except IndexError:
    sys.stderr.write("No start component at peak %f\n" % (start_y,))
    continue
  try:
    end_cc = rowccs[-1]
  except IndexError:
    sys.stderr.write("No end component at peak %f\n" % (end_y,))
    continue

  print "Start: ", start_cc.ul.x, start_cc.ul.y
  print "End: ", end_cc.ul.x, end_cc.ul.y

  if start_cc.label == end_cc.label:
    # The search is trivial, skip it
    pathccs = [start_cc]
  else:
    # Search for the shortest path between the start and end cc

    # flag that is set when path is found
#    done = threading.Event()

    paths = None

#    def _find_shortest_path():
    paths = g.dijkstra_shortest_path(start_cc.label)
#      done.set()

#    try:
      # start the thread
#    thread.start_new_thread(_find_shortest_path,())
#    except:
#      print "Error: unable to start thread."
#      continue

#    print "Waiting %f seconds..." % (SEARCH_WAIT_TIME,)
#    if not done.wait(SEARCH_WAIT_TIME):
#      print "Search too long, skipping..."
      # if the search did not finish on time, kill it
#      thread.exit()
#      continue # skip over the rest of the for loop
    
    if end_cc.label in paths.keys():
      print "Path from ", start_cc.label, "to ", end_cc.label, ": ",\
        paths[end_cc.label]
    else:
      print "No path from ", start_cc.label, "to ", end_cc.label
      continue
    
    dist, pathcclabels = paths[end_cc.label]
    pathccs = filter(lambda x: x.label in pathcclabels, subccs)
  
  for p in pathccs:
    rgbimg.highlight(p, RGBPixel(255,0,0))

# save the highlighted image
pathprepend = sys.argv[2]
imgpath = pathprepend+"/hl_"+time.strftime("%y-%m-%d_%H_%M_%S")\
  +"-"+os.path.basename(sys.argv[1])
print "Saving to: ", imgpath
rgbimg.save_PNG(imgpath)
