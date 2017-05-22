# $0 cmuwords ~/ang-hclg/g2p-model-2 ~/cmudict-ipa/cmudict/cmu.ipa.map.tsv
file=$1
model=$2
map=$3
./count_bigrams.py $file > $file.bigrams
g2p.py --model $model --apply $file.bigrams > $file.phonetic.tmp
cat $file.phonetic.tmp | sed -n '/.*\t..*/p' > $file.phonetic
cut -f1 $file.phonetic > $file.1
cut -f2- $file.phonetic > $file.2
[ ! -z $map ] && python3 cng2ipa.py $file.2 $map > $file.ipa.2 || cp $file.2 $file.ipa.2
paste $file.1 $file.ipa.2
