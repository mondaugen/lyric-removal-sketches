from gamera.core import *
import sys

init_gamera()

img = load_image(sys.argv[1]).to_onebit()

proj = img.projection_rows()

for p in proj:
  sys.stdout.write(str(p)+"\n")
