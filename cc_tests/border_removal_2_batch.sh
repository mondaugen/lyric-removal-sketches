#!/bin/bash
# tries to remove the borders on a directory of images
# crops the images instead of just whitening the edges

E_BADARGS=85
if [ ! -n "$1" ]
then
  echo "Usage: `basename $0` source-directory desination-directory"
  echo "  ul_x-fraction ul_y-fraction lr_x-fraction lr_y-fraction"
  echo "  These last 4 arguments are a decimal percentage (0-1) by"
  echo "  which to inwardly move the upper-left x and y and lower-"
  echo "  right x and y coordinates respectively, giving a bit more"
  echo "  crop."
  exit $E_BADARGS
fi

for image in `find $1`
do
  python border_removal_2.py $image $2 $3 $4 $5 $6
done

exit 0
