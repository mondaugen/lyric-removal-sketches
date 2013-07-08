#!/bin/bash
# tries to remove the borders on a directory of images

E_BADARGS=85
if [ ! -n "$1" ]
then
  echo "Usage: `basename $0` source-directory desination-directory"
  exit $E_BADARGS
fi

for image in `find $1`
do
  python border_removal_1.py $image $2
done

exit 0
