for f in `find $1 -name "*.wav"`; do
    d=`dirname $f`
    b=`basename $f`
    sox $f $d/16k_$b rate -v -s 16000
    mv $d/16k_$b $f
    echo Resampling $f
done

for f in `find $1 -name "*.mp3"`; do
    d=`dirname $f`
    b=`basename $f`
    sox $f $d/$b.wav rate -v -s 16000
    echo Resampling $f
done

