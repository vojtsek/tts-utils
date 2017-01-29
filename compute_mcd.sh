#!/bin/bash
# arguments: natural_recordings/ synthetic_recordings/
BIN_PATH="sptk/bin"
FRAMELEN=300
FRAMESHIFT=50
FFTLEN=512
NORMALIZE=1
MGCORDER=35
FREQWARP=0.42

LISTFILE="corpus.lst"
RESULTFILE="mcd.out"

function mgc {
# mgc path/to/wav
    base_fn=`basename $1`
    base_fn=${base_fn%.*}
    echo "Computing mel cepstral analysis of '$1'"
    ${BIN_PATH}/x2x +sf < "$1" | \
    ${BIN_PATH}/frame -l $FRAMELEN -p $FRAMESHIFT | \
    ${BIN_PATH}/window -l $FRAMELEN -L $FFTLEN -n $NORMALIZE | \
    ${BIN_PATH}/mcep -l $FFTLEN -m $MGCORDER -a $FREQWARP -e "1.0E-08" > "$2/${base_fn}.mgc"
}
if [[ -z $3 ]]; then
    for fn in $1/*.mfcc; do
        fn=`basename $fn`   
        ls $LISTFILE > /dev/null 2> /dev/null && rm $LISTFILE
        base_fn=${fn%.*}
        echo "${base_fn}" >> $LISTFILE
        echo "Comparing '$1/$fn' and '$2/$fn'"
        MCD=`cat $LISTFILE | xargs mcd/bin/get_mcd_dtw --ext mfcc --param_order $MGCORDER $1 $2 | tail -n1 | cut -d " " -f4`
        echo "$fn,${MCD}" >> $RESULTFILE
    done
else

    for fn in $1/*.wav; do
        fn=`basename $fn`   
        ls $LISTFILE > /dev/null 2> /dev/null && rm $LISTFILE
        mgc "$1/$fn" "$1"
        mgc "$2/$fn" "$2"
        base_fn=${fn%.*}
        echo "${base_fn}" >> $LISTFILE
        echo "Comparing '$1/$fn' and '$2/$fn'"
        MCD=`cat $LISTFILE | xargs mcd/bin/get_mcd_dtw --param_order $MGCORDER $1 $2 | tail -n1 | cut -d " " -f4`
        echo "$fn,${MCD}" >> $RESULTFILE
    done
fi
echo "Results written to '$RESULTFILE'"
