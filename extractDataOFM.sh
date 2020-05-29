#!/bin/bash
#
# for openflightmaps.org
#

srcDir='/home/jaja/data/download/vfrManual/openflightmaps.org/ofmx'
workDir='/home/ibisek/wqz/prog/android/vfrManual/app/src/main/assets/json'

source ./venv/bin/activate

files="$srcDir/*.ofmx"

for fn in $files
do
    regionCode=`echo $fn|sed 's/.*_\(.\{2\}\).*/\1/' | tr a-z A-Z`

    echo "Processing '$regionCode' -> '$fn'"
    
    python3 ./src/openflightmaps.py $regionCode $fn $workDir
done


deactivate

echo "done."
