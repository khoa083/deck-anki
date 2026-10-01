#!/bin/sh
# In trang lý thuyết (LEFT) của các unit: tools/show.sh BOOK U [U…]
B=$1; shift
for U in "$@"; do NN=$(printf %02d $U); echo "=== $B $U"; sed -n '/^### LEFT/,/^### RIGHT/p' src/${B}_u$NN.txt | grep -v '^### \|^EnglishVocabulary\|^English Vocabulary in Use' ; done
