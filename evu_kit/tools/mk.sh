#!/bin/sh
# tools/mk.sh BOOK U [U…] : điền Ngữ pháp còn trống (--auto) rồi make, chỉ in dòng lỗi/trùng/tổng
B=$1; shift
for U in "$@"; do NN=$(printf %02d $U); python3 tools/fixg.py data/${B}_u$NN.txt --auto; done
python3 evu.py make $B "$@" 2>&1 | grep -E "LỖI|đã có|mục \|"
