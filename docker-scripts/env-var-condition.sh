#!/bin/bash
for f in results/*; do
  if [ -s $f ]; then
    python /scripts/failed-check-teams.py $1
    ./cl-output.sh
    exit 0
  fi
done
python /scripts/passed-check-teams.py $1
