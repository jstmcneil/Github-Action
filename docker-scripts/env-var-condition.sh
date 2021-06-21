#!/bin/bash
for f in results/*; do
  echo "1: $1"
  echo "2: ${2:-}"
  if [ -s $f ]; then
    python /scripts/failed-check-teams.py ${2:"default"} ${1:-}
    exit 1
  fi
done
python /scripts/passed-check-teams.py ${2:"default"} ${1:-}
exit 0
