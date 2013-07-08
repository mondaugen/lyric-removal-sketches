# find the minimum number of 0 separating a 1 and a 2

import sys

strip = [1,0,2,0,0,0,2,0,0,1] # minimum distance should be 1
strip2 = [0,0]

def get_min_dist_in_strip(strip):
  mindist = sys.maxint
  dist = 0
  
  col = 0
  width = len(strip)
  
  # skip over whitespace on the edge
  while col < width and strip[col] == 0:
    col = col + 1
  lr = (-1,-1)
  
  if col < width:
    state = strip[col]
    l = col
    r = col
  else:
    return (-1,lr) # strip empty

  
  while col < width:
    if strip[col] == 0:
      dist = dist + 1
    elif strip[col] == state:
      dist = 0
      l = col
    else:
      r = col
      if dist < mindist:
        mindist = dist
        lr = (l,r)
      l = col
      dist = 0
      state = strip[col]
    col = col + 1
  return (mindist,lr)

print "Minimum distance: ", get_min_dist_in_strip(strip)
