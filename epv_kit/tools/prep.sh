#!/bin/sh
# Chuẩn bị 1 unit Intermediate: ảnh trang + đáp án + Mini dictionary
N=$1; NN=$(printf %02d $N)
python3 tools/page_img.py int $N both >/dev/null; ls /tmp/pages/int_u${NN}_*
sed -n '/### KEY/,$p' src/int_u$NN.txt
