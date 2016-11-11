LISTFILE=lf0s.lst
RESULTFILE=lf0.out
# arguments: natural_recordings/ synthetic_recordings/
for fn in $1/*.lf0; do
    fn=`basename $fn`   
    ls $LISTFILE > /dev/null 2> /dev/null && rm $LISTFILE
    base_fn=${fn%.*}
    echo "${base_fn}" >> $LISTFILE
    echo "Comparing '$1/$fn' and '$2/$fn'"
    cat $LISTFILE | xargs mcd/bin/get_lf0d_dtw.py --ext lf0 --param_order 1 $1 $2
    LF0=`cat $LISTFILE | xargs mcd/bin/get_lf0d_dtw.py --ext lf0 --param_order 1 $1 $2 | tail -n1 | cut -d " " -f4`
    echo "$fn ${LF0}" >> $RESULTFILE
done
#rm $1/*.mgc $2/*.mgc
echo "Results written to '$RESULTFILE'"
