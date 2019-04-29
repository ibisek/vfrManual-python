#!/bin/bash

TMPDIR='/tmp/00'

mkdir -p $TMPDIR
#cd $TMPDIR


## lis.rlp.cz data:
function dataRLP {
wget -P $TMPDIR http://lis.rlp.cz/vfrmanual/actual/20190425_1.zip
cd $TMPDIR
unzip *.zip
cd -
./extractDataRLP.sh
rm -rf $TMPDIR/*
}


## Databaze letist data:
function dataDL {
wget -P $TMPDIR http://www.aerobaze.cz/gps/DatabazeLetistGPS_28mar19.zip
./extractDataDL.sh
rm -rf $TMPDIR/*
}


## OFM data:
function dataOFM {
wget -P $TMPDIR http://snapshots.openflightmaps.org/live/1806/aixm45/lkaa/latest/aixm_lk.zip
wget -P $TMPDIR http://snapshots.openflightmaps.org/live/1806/aixm45/lzbb/latest/aixm_lz.zip
wget -P $TMPDIR http://snapshots.openflightmaps.org/live/1806/aixm45/epww/latest/aixm_ep.zip

cd $TMPDIR

unzip -p aixm_lk.zip aixm_lk/embedded/aixm_lk.xml > aixm_lk.xml
unzip -p aixm_lz.zip aixm_lz/embedded/aixm_lz.xml > aixm_lz.xml
unzip -p aixm_ep.zip aixm_ep/embedded/aixm_ep.xml > aixm_ep.xml

cd -

./extractDataOFM.sh

rm -rf $TMPDIR/*
}


dataRLP
dataDL
dataOFM


echo "Done. Finished."