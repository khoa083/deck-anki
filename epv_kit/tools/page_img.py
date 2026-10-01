#!/usr/bin/env python3
"""Render trang sách thành PNG để KIỂM BẰNG MẮT (bắt buộc với Intermediate vì text là OCR).
Dùng: python3 tools/page_img.py adv|int UNIT [left|right|both]  -> in đường dẫn PNG, rồi mở bằng công cụ xem ảnh.
Cần PDF trong books/ (xem PROMPT.md: bước chuẩn bị)."""
import sys, os, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = {"adv": os.path.join(KIT, "books", "adv.pdf"), "int": os.path.join(KIT, "books", "int.pdf")}
book, unit = sys.argv[1], int(sys.argv[2]); which = sys.argv[3] if len(sys.argv) > 3 else "left"
first = (8 + 2 * unit) if book == "adv" else (6 + 2 * unit)     # trang 1-based
pages = {"left": [first], "right": [first + 1], "both": [first, first + 1]}[which]
os.makedirs("/tmp/pages", exist_ok=True)
for p in pages:
    out = f"/tmp/pages/{book}_u{unit:02d}_p{p}"
    subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", "110", "-png", "-singlefile", PDF[book], out], check=True)
    print(out + ".png")
