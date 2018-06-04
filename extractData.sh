#!/bin/bash

srcDir='/home/ibisek/download/vfrManual/unpacked/actual'
outDir='/home/ibisek/wqz/prog/android/vfrManual/app/src/main/assets'

#srcDir='/tmp/00/2'
#outDir='/tmp/00/b'

lang='cz'
#lang='en'

files=`ls $srcDir/lk*$lang.html`

for f in $files
do
    echo "processing $f"
    python3 ./src/html2json.py $f $outDir/json
done

# copy images:
cp $srcDir/ad/*adc* $outDir/adc/
cp $srcDir/ad/*voc* $outDir/voc/

echo "done."
