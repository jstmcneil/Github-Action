#!/bin/bash
for f in results/*; do
  if [ -s $f ]; then
	  python /scripts/failed-check-teams.py $argv[1]
    exit 0
  fi
done
python /scripts/passed-check-teams.py $argv[1]
