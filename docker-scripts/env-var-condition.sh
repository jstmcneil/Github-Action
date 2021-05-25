#!/bin/bash
for f in results/*; do
  if [ -s $f ]; then
	  python failed-check-teams.py argv[1]
    exit 0
  fi
done
python passed-check-teams.py argv[1]