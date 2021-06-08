#!/bin/bash
for f in results/*; do
  if [ -s $f ]; then
  	if $3:
	  	python /scripts/failed-check-teams.py $1
	  fi
    exit 0
  fi
done

if $3:
	python /scripts/passed-check-teams.py $1
fi
