#!/bin/bash
echo $1
python_script="/scripts/python-checkforcfn.py"
# Replace w/ paramatarized ruleset.
outputted="/ruleset_migrated.guard"
if ! [[ -n $outputted ]]; then
  echo "No rule-file found w/ %ruleset-file% name."
  exit 1
fi

mkdir results
find . -type f \( -iname \*.yaml -o -iname \*.json -o -iname \*.yml \) -follow -print0 | while read -d $'\0' f
do
  base_name="$(basename -- $f)"
  echo $base_name
  python $python_script $f
  ret=$?
  if [[ $ret -eq 0 ]]; then
  	/scripts/cfn-guard-data-wrangle.sh $outputted $f > results/${base_name}.txt
    numb="$(cat $results/${base_name}.txt | grep "Resource \[" | wc -l)"
    echo -e "\nTotal Failures: "  | sed -e '$s%$%'"$numb"'%' >> results/${base_name}.txt
  fi
done
echo -e "\n"
# Runs next step w/ webhook attached.
#if [ -z "$3" ]; then
 # bash /scripts/env-var-condition.sh $2
#else
 # bash /scripts/env-var-condition.sh $3 $2
#fi
