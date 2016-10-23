for txt in $1/*; do
    fn=`basename $txt`
    fn=${fn%.*}
    ls predicted > /dev/null 2> /dev/null || mkdir predicted
    ls synthesized > /dev/null 2> /dev/null || mkdir synthesized
    ./txt2sp.py $txt
    echo "Predicting $fn"
    mv /home/vojtech/marytts-5.2beta3/target/marytts-5.2-beta3/bin/MGC.bin predicted/$fn.mgc
    mv mary.wav $fn.wav
    ./mcep.sh $fn.wav synthesized
    rm $fn.wav
done
