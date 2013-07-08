#!/bin/bash
# script that tries to find the lyrics in all the images in a directory, putting
# the results in another directory. Lyrics are highlighted in red.

E_BADARGS=85
if [ ! -n "$6" ]
then
  echo "Usage: `basename $0` source-directory desination-directory"
  echo "min-y-threshold number-of-searches negative-height-bound"
  echo "positive-height-bound"
  echo "example `basename $0` ./source ./dest 400 40 200 200"
  echo "will search for peaks in horizontal projections with a minimum"
  echo "threshold of 400 and do 40 searches -200 to 200 pixels above and"
  echo "below each peak"
  exit $E_BADARGS
fi

for image in `find $1`
do
  python ccgtsp_functional_projections_3.py $image $2 $3 $4 $5 $6
done

exit 0
