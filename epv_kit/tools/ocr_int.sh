#!/bin/sh
# OCR lại PDF Intermediate (chỉ cần nếu muốn tạo lại src/int_*). ~1-3 giây/trang, chạy theo đợt < 5 phút/lệnh.
# Dùng: sh tools/ocr_int.sh books/int.pdf ocr
PDF=$1; OUT=$2; mkdir -p $OUT
[ -f $OUT/p-001.pgm ] || pdftoppm -r 300 -gray $PDF $OUT/p
S=$(date +%s)
for f in $OUT/*.pgm; do [ -s "$f.t.txt" ] && continue; [ $(( $(date +%s)-S )) -gt 270 ] && echo "chạy lại lệnh để tiếp tục" && exit 0; tesseract "$f" "$f.t" --psm 3 >/dev/null 2>&1; done
echo "OCR xong: $(ls $OUT/*.t.txt | wc -l) trang"
