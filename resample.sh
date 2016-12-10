for f in `find backers -name "*.wav"`; do
    d=`dirname $f`
    b=`basename $f`
    sox $f $d/16k_$b rate -v -s 16000
    echo Resampling $f
done
