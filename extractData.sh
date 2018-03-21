#!/bin/bash

srcDir='/home/ibisek/download/vfrManual/unpacked/actual'
outDir='/home/ibisek/wqz/prog/android/vfrManualCZ/app/src/main/assets/json'
lang='cz'
#lang='en'

files=`ls $srcDir/lk*$lang.html`

for f in $files
do
    echo "processing $f"
    python3 ./src/html2json.py $f $outDir
done

echo "done."
