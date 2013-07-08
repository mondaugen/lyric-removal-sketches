#!/bin/bash
# script that tries to find the lyrics in all the images in a directory, putting
# the results in another directory. Lyrics are highlighted in red.

E_BADARGS=85
if [ ! -n "$1" ]
then
  echo "Usage: `basename $0` source-directory desination-directory time-out-time"
  exit $E_BADARGS
fi

for image in `find $1`
do
  python cc_graph_test_shortest_path_peak_multi_split_timeout.py $image $2 $3
done

exit 0
