#!/bin/bash
#
# for DATABAZE LETIST
#

srcDir='/tmp/00'
outDir='/tmp/00'

unzip -o $srcDir/*.zip -d $outDir/ 

filename=`ls $outDir/*gpx`
#echo "FN: $filename"

tmpFile="ulonly.xml"
grep "Ultralight Area" $filename > $outDir/$tmpFile

python3 ./src/xml2json.py $outDir/$tmpFile $outDir

echo "done."
