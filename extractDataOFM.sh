#!/bin/bash
#
# for openflightmaps.org
#

srcDir='/tmp/00'
workDir='/home/ibisek/wqz/prog/android/vfrManual/app/src/main/assets/json'


echo "Processing LK.."
python3 ./src/openflightmaps.py LK $srcDir/aixm_lk.xml $workDir
echo "Processing LZ.."
python3 ./src/openflightmaps.py LZ $srcDir/aixm_lz.xml $workDir
echo "Processing EP.."
python3 ./src/openflightmaps.py EP $srcDir/aixm_ep.xml $workDir
#echo "Processing ED.."
#python3 ./src/openflightmaps.py EP $srcDir/aixm_ed.xml $workDir
#echo "Processing LO.."
#python3 ./src/openflightmaps.py EP $srcDir/aixm_lo.xml $workDir


echo "done."
