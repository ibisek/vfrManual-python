#!/bin/bash
#
# for openflightmaps.org
#

srcDir='/home/jaja/data/download/vfrManual/openflightmaps.org/ofmx'
workDir='/home/ibisek/wqz/prog/android/vfrManual/app/src/main/assets/json'

source ./venv/bin/activate

echo "Processing LK.."
python3 ./src/openflightmaps.py LK $srcDir/ofmx_lk.ofmx $workDir
echo "Processing LZ.."
python3 ./src/openflightmaps.py LZ $srcDir/ofmx_lz.ofmx $workDir
echo "Processing EP.."
python3 ./src/openflightmaps.py EP $srcDir/ofmx_ep.ofmx $workDir
echo "Processing ED.."
python3 ./src/openflightmaps.py ED $srcDir/ofmx_ed.ofmx $workDir
echo "Processing LO.."
python3 ./src/openflightmaps.py LO $srcDir/ofmx_lo.ofmx $workDir

deactivate

echo "done."
