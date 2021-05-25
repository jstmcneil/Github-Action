#!/bin/bash
pwd
ls -a
python_script="/scripts/python-checkforcfn.py"
# Replace w/ paramatarized ruleset.
outputted="/global_policies.ruleset"
if ! [[ -n $outputted ]]; then
  echo "No rule-file found w/ %ruleset-file% name."
  exit 1
fi

mkdir results
find . -type f \( -iname \*.yaml -o -iname \*.json -o -iname \*.yml \) -follow -print0 | while read -d $'\0' f
do
  base_name="$(basename -- $f)"
  base_name=$(echo "$base_name" | cut -f 1 -d '.')
  python $python_script $f
  ret=$?
  if [[ $ret -eq 0 ]]; then
  	cfn-guard check -r $outputted -t $f >> results/${base_name}.txt
  fi
done

echo "##RESULTS PAGE##"
ls results/
# Runs next step w/ webhook attached.
bash env-var-condition.sh $argv[1]
