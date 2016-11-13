#!/bin/bash
BIN_PATH="bin"
FRAMELEN=400
FRAMESHIFT=80
FFTLEN=512
NORMALIZE=0
MGCORDER=34
FREQWARP=0.42

# mgc path/to/wav
base_fn=`basename $1`
base_fn=${base_fn%.*}
echo "Computing mel cepstral analysis of '$1'"
${BIN_PATH}/x2x +sf < "$1" | \
${BIN_PATH}/frame -l $FRAMELEN -p $FRAMESHIFT | \
${BIN_PATH}/window -l $FRAMELEN -L $FFTLEN -n $NORMALIZE -w 1 | \
${BIN_PATH}/mcep -l $FFTLEN -m $MGCORDER -a $FREQWARP -e "1.0E-08" > "$2/${base_fn}.mgc"
