#!/bin/bash
for f in results/*; do
  if [ -s $f ]; then
    python /scripts/failed-check-teams.py ${1:-} ${2:-}
    exit 1
  fi
done
python /scripts/passed-check-teams.py ${2:-}
exit 0
