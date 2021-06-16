#! /bin/bash
for f in results/*
do
    if [ -s $f ]; then
        var=1
        NAME=$(echo $f | cut -d '.' -f 1,2 | cut -d '/' -f2)
        echo -e "\033[37mErrors for \033[33m[$NAME]\033[37m CloudFormation Template:"
        echo -e "\033[37m---------------------\033[0m"
        echo -e $(cat $f | awk 'NF' | sed -e 's,\[,\\033\[33m[,g' | sed -e 's,\],]\\033\[37m,g' | sed -e 's,^,\\033[37m,' | sed 's/$/\\n/' | sed -e 's/^ *//g') | sed 's/^ *//g' | awk 'NF'
        echo -e "\033[37m---------------------\033[0m\n"
    fi
done
if [ $var ]; then
    echo "::error::You have failed some basline policies. All failures are listed in the Output Data step."
    exit 1
fi
