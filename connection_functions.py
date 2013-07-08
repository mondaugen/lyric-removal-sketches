# some functions for connecting components

from gamera.core import *
from gamera import graph
from gamera import graph_util
import sys
import array

def make_labeled_image(img,ccs,gapval):
  '''
  Returns an image with pixel values set to the connected component's labels.
  '''
  result = Image(img.ul, img.lr)
  result.fill(gapval)
  for cc in ccs:
    result.highlight(cc,cc.label)
  return result

def translate_strip(strip,homecc,gapval):
  '''
  Translates the strip (a row from the labeled image) in to a strip where each
  pixel is either 1 if it belongs to the home connected component (homecc),
  gapval if it is whitespace or 2 if it is not the home connected component.
  '''
  result = [gapval for i in xrange(len(strip))]
  for i in xrange(len(strip)):
    if strip[i] == homecc.label:
      result[i] = 1
    elif strip[i] == gapval:
      pass
    else:
      result[i] = 2
  return result

def get_min_dist_in_strip(strip, gapval):
  mindist = sys.maxint
  dist = 0
  
  col = 0
  width = len(strip)
  
  # skip over whitespace on the edge
  while col < width and strip[col] == gapval:
    col = col + 1
  lr = (-1,-1)
  
  if col < width:
    state = strip[col]
    l = col
    r = col
  else:
    return (-1,lr) # strip empty
  
  while col < width:
    if strip[col] == gapval:
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

def all_horizontal_bridges_in_strip(strip, gapval):
  '''
  Returns a list of (x0,x1) pairs that are the horizontal bridges extending from
  a 1 to a 2 separated by gapvals in the strip.
  '''
  index_pairs=[]
  width = len(strip)
  state = gapval
  i = 0
  while strip[i] == gapval:
    i = i + 1
  if i < width:
    state = strip[i]
  else:
    return index_pairs
  l = i
  while i < width:
    if strip[i] == 0:
      pass
    elif strip[i] == state:
      l = i
    else:
      index_pairs.append((l, i))
      l = i
      state = strip[i]
    i = i + 1
  return index_pairs

def states_from_bridge_pairs(strip, bridges):
  result = []
  for x, y in bridges:
    result.append((strip[x], strip[y]))
  return result


def shortest_horizontal_bridge(a, b):
  '''
  Returns a tuple (x0,y0,x1,y1) describing a line that is the shortest
  horizontal bridge between two connected components. Raises StandardError when
  no horizontal bridge exists between them. Orig is the image from where the ccs
  are from. The coordinates returned are relative to this image.
  '''

  # make an image contatining the two components
  newul = Point(0,0)

  if a.ul.x < b.ul.x:
    newul.x = a.ul.x
  else:
    newul.x = b.ul.x

  if a.ul.y < b.ul.y:
    newul.y = a.ul.y
  else:
    newul.y = b.ul.y

  newlr = Point(0,0)

  if a.lr.x > b.lr.x:
    newlr.x = a.lr.x
  else:
    newlr.x = b.lr.x

  if a.lr.y > b.lr.y:
    newlr.y = a.lr.y
  else:
    newlr.y = b.lr.y

  tmpimg = Image(newul, newlr, GREYSCALE)
  tmpimg.highlight(a, 1)
  tmpimg.highlight(b, 2)
  mindist = sys.maxint
  minlr = (-1,-1)
  miny = -1
  for i in xrange(tmpimg.nrows):
    strip = [tmpimg.get(Point(j,i)) for j in xrange(tmpimg.ncols)]
    dist, lr = get_min_dist_in_strip(strip,255)
    found = 0
    if dist != -1:
      if dist < mindist:
        mindist = dist
        minlr = lr
        miny = i

  if minlr[0] == -1:
    raise StandardError # No bridge exists

  return (minlr[0] + newul.x, miny + newul.y, minlr[1] + newul.x, miny + newul.y)

def make_horizontal_cc_graph(img,ccs):
  '''
  Returns a graph representing the connected components in the image, connected
  by horizontal lines extending out from each connected component. These lines
  stop once obstructed by another connected component.
  '''
  g = graph.Graph(graph.UNDIRECTED)
  tmpimg = make_labeled_image(img,ccs,0)
  for cc in ccs:
    if ((cc.ul.x >= img.ul.x) and (cc.ul.y >= img.ul.y) \
        and (cc.lr.x <= img.lr.x) and (cc.lr.y <= img.lr.y)):
      y_offset = cc.ul.y - img.offset_y
      cc_height = cc.nrows
      # Array of component bridges
      component_bridges = dict()
      # For eachstrip in the image, translate the strip into home, neighbour and
      # whitespace, then find bridges, translate bridges, and add the bridges to
      # the component_bridges array
      for row in xrange(y_offset, y_offset + cc_height):
        strip = [tmpimg.get((i,row)) for i in xrange(tmpimg.ncols)]
        transstrip = translate_strip(strip,cc,0)
        transbridges = all_horizontal_bridges_in_strip(transstrip,0)
        states = states_from_bridge_pairs(strip,transbridges)
        for x, s in zip(transbridges, states):
          x0, x1 = x
          s0, s1 = tuple(sorted(s))
          # only add the state transition if it is not already in the
          # component_bridges dictionary or its bridge is shorter than the one
          # already in the dictionary
          blen = abs(x1 - x0) - 1
          if (s0,s1) in component_bridges.keys():
            if blen < component_bridges[(s0,s1)]:
              component_bridges[(s0,s1)] = blen
          else:
            component_bridges[(s0,s1)] = blen
          #cb = dict()
          #cb["x0"] = x0
          #cb["x1"] = x1
          #cb["y0"] = row
          #cb["y1"] = row
          #cb["s0"] = s0
          #cb["s1"] = s1
          #component_bridges.append(cb)
      # Now we populate the graph with the bridges we found
      # Nodes are the component ids, edge costs are the bridge lengths (horizontal
      # distances between ccs)
      # The -1 in calculating the distance is because we are interested in how
      # many white space pixels are between two components, not the difference in
      # pixel x-coordinates
      for k in component_bridges.keys():
        s0, s1 = k
        l = component_bridges[k]
        if g.has_edge(s0,s1):
          pass # don't add, we've already added this edge and it's the shortest
        else:
          g.add_edge(s0,s1,l)
  return g

