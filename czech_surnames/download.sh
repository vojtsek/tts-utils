for letter in {A..Z}; do
    echo $letter
    curl http://www.kdejsme.cz/seznam/jmeno/$letter > tmp && cat tmp | grep "jmeno" | cut -d'>' -f3 | sed 's|</a||' >> surnames.lst
done
