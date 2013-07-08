from gamera.core import *
import sys
import random
import time

init_gamera()

img = load_image(sys.argv[1])

onebit = img.to_onebit()

structure = Image(Point(0,0),Point(4,8), ONEBIT)

structure.fill(1)

result = onebit.erode_with_structure(structure, Point(2,4))

result.save_PNG(sys.argv[2])
