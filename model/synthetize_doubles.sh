synthetize() {
    echo $1 > input_trn
    ../txt2wav.py input_trn $2
}
cat $1 | while read bebest trn orig best; do
    #synthetize $orig $orig.orig.wav
    #synthetize "<phoneme alphabet=\"ipa\" ph=\"$best\">$orig</phoneme>" $orig.best.wav
    #synthetize "<phoneme alphabet=\"ipa\" ph=\"$trn\">$orig</phoneme>" $orig.trn.wav
    synthetize "<phoneme alphabet=\"ipa\" ph=\"$bebest\">$orig</phoneme>" $orig.thebest.wav
done
