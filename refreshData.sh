#!/bin/bash

TMPDIR='/tmp/00'

mkdir -p $TMPDIR
#cd $TMPDIR


## lis.rlp.cz data:
function dataRLP {
wget -P $TMPDIR https://aim.rlp.cz/vfrmanual/actual/20200326_1.zip
cd $TMPDIR
unzip *.zip
cd -
./extractDataRLP.sh
rm -rf $TMPDIR/*
}


## Databaze letist data:
function dataDL {
wget -P $TMPDIR http://aerobaze.cz/gps/DatabazeLetistGPS_26mar20.zip
./extractDataDL.sh
rm -rf $TMPDIR/*
}


## OFM data:
function dataOFM {
#wget -P $TMPDIR http://snapshots.openflightmaps.org/live/1806/aixm45/lkaa/latest/aixm_lk.zip
#wget -P $TMPDIR http://snapshots.openflightmaps.org/live/1806/aixm45/lzbb/latest/aixm_lz.zip
#wget -P $TMPDIR http://snapshots.openflightmaps.org/live/1806/aixm45/epww/latest/aixm_ep.zip
#wget -P $TMPDIR http://snapshots.openflightmaps.org/live/1806/aixm45/epww/latest/aixm_ed.zip
#wget -P $TMPDIR http://snapshots.openflightmaps.org/live/1806/aixm45/epww/latest/aixm_lo.zip

#cd $TMPDIR

#unzip -p aixm_lk.zip aixm_lk/embedded/aixm_lk.xml > aixm_lk.xml
#unzip -p aixm_lz.zip aixm_lz/embedded/aixm_lz.xml > aixm_lz.xml
#unzip -p aixm_ep.zip aixm_ep/embedded/aixm_ep.xml > aixm_ep.xml
#unzip -p aixm_ep.zip aixm_ep/embedded/aixm_ep.xml > aixm_ed.xml
#unzip -p aixm_ep.zip aixm_ep/embedded/aixm_ep.xml > aixm_lo.xml

cd /home/jaja/data/download/vfrManual/openflightmaps.org/ofmx
unzip -p ofmx_ed.zip ofmx_ed/embedded/ofmx_ed.ofmx > ofmx_ed.ofmx
unzip -p ofmx_ep.zip ofmx_ep/embedded/ofmx_ep.ofmx > ofmx_ep.ofmx
unzip -p ofmx_lk.zip ofmx_lk/embedded/ofmx_lk.ofmx > ofmx_lk.ofmx
unzip -p ofmx_lo.zip ofmx_lo/embedded/ofmx_lo.ofmx > ofmx_lo.ofmx
unzip -p ofmx_lz.zip ofmx_lz/embedded/ofmx_lz.ofmx > ofmx_lz.ofmx
cd -

./extractDataOFM.sh

#rm -rf $TMPDIR/*
}


#dataRLP
#dataDL
dataOFM


echo "Done. Finished."