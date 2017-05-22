#! /bin/bash

WD=`pwd`
dir=$1
labels=$2
if [ $# -lt 3 ]; then
    cd $dir
    rm *.cd*
    rm Dataset.bin coeffs.bin.*
    ~/tts-utils/MCD/prepare_dataset.py $labels
    for fold in {1..8}; do
        ~/tts-utils/MCD/regr.py $fold > r2.$fold
        ./extract.sh $fold
    done
else
    cd $WD
    fold=$3
    ./observe.py $dir/*.cd.$fold
    dmp=mgc-dump/$(ls -rt mgc-dump | tail -n1)
    ./compute_correlation.py $dmp $dmp $labels
    mv corr.png $dir/corr.$fold.png
fi
