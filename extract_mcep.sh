#!/bin/bash
BIN_PATH=/home/vojta/SPTK-3.10/bin
FRAMELEN=200
FRAMESHIFT=40
FFTLEN=512
NORMALIZE=1
MGCORDER=34
FREQWARP=0.42

# mgc path/to/wav
base_fn=`basename $1`
base_fn=${base_fn%.*}
echo "Computing mel cepstral analysis of '$1'"
${BIN_PATH}/x2x/x2x +sf < "$1" | \
${BIN_PATH}/frame/frame -l $FRAMELEN -p $FRAMESHIFT | \
${BIN_PATH}/window/window -l $FRAMELEN -L $FFTLEN -n $NORMALIZE -w 1 | \
${BIN_PATH}/mcep/mcep -l $FFTLEN -m $MGCORDER -a $FREQWARP -e "1.0E-08" > "${1%.*}.mfcc"
