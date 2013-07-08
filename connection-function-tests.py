from connection_functions import *

from gamera.core import *
import sys

init_gamera()

# Only use this on an image you know has two ccs

img = load_image(sys.argv[1])

ccs = img.cc_analysis()

print shortest_horizontal_bridge(ccs[0],ccs[1])
