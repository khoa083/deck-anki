"""Dựng lại Mini dictionary Intermediate từ OCR 300 dpi (tesseract psm 3, trang PDF 179–202 → tools/int_minidict_ocr300.txt).
Mỗi mục là một khối cách nhau bởi dòng trống, kết thúc bằng danh sách số unit. Ghi đè phần MINI DICTIONARY trong src/int_uNN.txt.
Dùng: python3 tools/int_minidict.py [--write]"""
import re, os, sys, collections
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = open(os.path.join(KIT, "tools", "int_minidict_ocr300.txt"), encoding="utf-8").read()
raw = re.sub(r"(?m)^\s*(\d{3}|English Phrasal Verbs in Use Intermediate|Mini dictionary)\s*$", "", raw)
def parse_lines(raw):
    out, buf = [], []
    for line in raw.splitlines():
        line = line.strip()
        if not line: continue
        buf.append(line)
        m = re.search(r"(?<![A-Za-z\-])((?:\d{1,2}\s*,\s*)*\d{1,2})\s*$", line)
        if m and re.search(r"[a-z]{3}", " ".join(buf)):
            units = [int(x) for x in re.findall(r"\d+", m.group(1)) if 1 <= int(x) <= 70]
            if units:
                txt = " ".join(buf); out.append((txt[:len(txt) - (len(line) - m.start())].strip(), units)); buf = []
    return out
def parse_blocks(raw):
    out, buf = [], []
    for block in re.split(r"\n\s*\n", raw):
        line = " ".join(block.split())
        if not line: continue
        buf.append(line)
        m = re.search(r"((?:\d{1,2}\s*,\s*)*\d{1,2})\s*$", " ".join(buf))
        if m:
            txt = " ".join(buf); units = [int(x) for x in re.findall(r"\d+", m.group(1)) if 1 <= int(x) <= 70]
            if units: out.append((txt[:m.start()].strip(), units)); buf = []
    return out
# hợp hai cách tách (mỗi cách sót mục ở chỗ OCR mất/thừa dòng trống); khử trùng theo 30 ký tự đầu
entries, seen = [], set()
for t, us in parse_lines(raw) + parse_blocks(raw):
    k = re.sub(r"\W+", "", t.lower())[:30]
    if k in seen: continue
    seen.add(k); entries.append((t, us))
by = collections.defaultdict(list)
for t, us in entries:
    for u in us: by[u].append(f"- {t} ({', '.join(map(str, us))})")
print(len(entries), "mục;", "unit trống:", [u for u in range(1, 71) if not by[u]])
if "--write" in sys.argv:
    for u in range(1, 71):
        p = os.path.join(KIT, "src", f"int_u{u:02d}.txt"); s = open(p, encoding="utf-8").read()
        s = re.sub(r"### MINI DICTIONARY.*$", "### MINI DICTIONARY (OCR lại 300 dpi, mỗi dòng = 1 mục; số trong ngoặc = các unit):\n" + "\n".join(by[u]), s, flags=re.S)
        open(p, "w", encoding="utf-8").write(s)
    print("đã ghi 70 file src/int_*.txt")
