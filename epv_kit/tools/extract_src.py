#!/usr/bin/env python3
"""Trích nguồn cho từng unit của 2 sách English Phrasal Verbs in Use (2nd edition) -> src/<book>_uNN.txt

Dùng: python3 tools/extract_src.py <advanced.pdf> <intermediate_ocr_dir> <out_dir>

- Advanced (PDF có lớp chữ): unit n = PDF index 0-based 7+2n (lý thuyết), 8+2n (bài tập);
  đáp án: index 129..164 (mốc "Unit n"); Mini dictionary: index 165..193.
- Intermediate (PDF scan): cần OCR trước bằng tools/ocr_int.sh -> <ocr_dir>/p-NNN.pgm.t.txt (NNN = trang PDF 1-based).
  unit n = trang 6+2n (lý thuyết), 7+2n (bài tập); đáp án trang 148..178; Mini dictionary 179..202.
  Text OCR có lỗi (ký tự lạ, mất chữ, cột bị trộn) -> LUÔN kiểm lại bằng ảnh trang (tools/page_img.py).
Mỗi file src gồm: BOLD (chỉ Advanced) / LEFT PAGE / RIGHT PAGE / KEY / MINI DICTIONARY.
"""
import sys, os, re

def bold_phrases(page):
    out, cur = [], []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                isb = ("Bold" in s["font"] or "Semibold" in s["font"]) and 8 < s["size"] < 11
                if isb and not re.fullmatch(r"\s*\d+\s*", s["text"]):
                    cur.append(s["text"])
                elif cur and s["text"].strip() and not re.fullmatch(r"[\d\s.,]+", s["text"]):
                    out.append("".join(cur)); cur = []
        if cur: out.append("".join(cur)); cur = []
    out = [re.sub(r"\s+", " ", x).strip(" ,.;:\t") for x in out]
    return [x for x in out if x and len(x) > 2 and x not in ("Tip", "Exercises")]

def split_key(text, n_units):
    """text toàn bộ phần Key -> {unit: text}. Mốc 'Unit n' (Advanced) hoặc số bài tập 'n.1' (Intermediate)."""
    res = {}
    marks, last = [], 0
    for m in re.finditer(r"(?m)^\s*Unit\s+(\d{1,2})\b", text):
        u = int(m.group(1))
        if u == last + 1: marks.append((m.start(), u)); last = u
    if len(marks) < n_units // 2:  # OCR: dùng số bài tập 'n.1'
        marks, last = [], 0
        for m in re.finditer(r"(?m)^\s*(\d{1,2})\.1\b", text):
            u = int(m.group(1))
            if u == last + 1: marks.append((m.start(), u)); last = u
    for i, (pos, u) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        res[u] = text[pos:end].strip()
    return res

def mini_dict_adv(text):
    ents = []
    for m in re.finditer(r"([^\n\u2002]+(?:\n[^\n\u2002]+)?)\u2002\s*(.+?)\u2002\s*([\d, ]+)\s*(?:\n|$)", text, re.S):
        head = re.sub(r"\s+", " ", m.group(1)).strip(); d = re.sub(r"\s+", " ", m.group(2)).strip()
        units = [int(x) for x in re.findall(r"\d+", m.group(3))]
        ents.append((head, d, units))
    return ents

def main(apdf, ocr_dir, od):
    import pymupdf
    os.makedirs(od, exist_ok=True)
    # ---------------- Advanced
    d = pymupdf.open(apdf)
    key = split_key("\n".join(d[i].get_text() for i in range(129, 165)), 60)
    md = mini_dict_adv("\n".join(re.sub(r"(?m)^\s*(\d{3}\s*)?\n?English Phrasal Verbs in Use Advanced\s*$|^\s*\d{3}\s*$", "", d[i].get_text()) for i in range(165, 194)))
    for u in range(1, 61):
        pg, ex = d[7 + 2 * u], d[8 + 2 * u]
        ents = [f"- {h} — {df} (units {', '.join(map(str, us))})" for h, df, us in md if u in us]
        with open(f"{od}/adv_u{u:02d}.txt", "w", encoding="utf-8") as f:
            f.write(f"# English Phrasal Verbs in Use Advanced (2nd ed.) – Unit {u} – trang sách {pg.number - 2}-{ex.number - 2}\n")
            f.write("### BOLD (cụm in đậm trên trang lý thuyết – gợi ý, có lẫn tên người/tiêu đề, cần lọc):\n")
            f.write("\n".join("- " + b for b in bold_phrases(pg)))
            f.write("\n\n### LEFT PAGE (lý thuyết):\n" + pg.get_text())
            f.write("\n\n### RIGHT PAGE (bài tập – tham khảo ví dụ):\n" + ex.get_text())
            f.write("\n\n### KEY (đáp án bài tập của unit này):\n" + key.get(u, "(không tách được – xem PDF)"))
            f.write("\n\n### MINI DICTIONARY (định nghĩa chính thức của sách cho các mục thuộc unit này):\n" + ("\n".join(ents) or "(trống)"))
    # ---------------- Intermediate (OCR)
    def page(p):
        fp = os.path.join(ocr_dir, f"p-{p:03d}.pgm.t.txt")
        return open(fp, encoding="utf-8").read() if os.path.exists(fp) else ""
    ikey = split_key("\n".join(page(p) for p in range(148, 179)), 70)
    idict = "\n".join(page(p) for p in range(179, 203))
    IENTS, buf = [], []
    for line in idict.splitlines():
        l = line.strip()
        if not l or re.fullmatch(r"(English Phrasal Verbs in Use Intermediate|Mini dictionary|\d{3})", l): continue
        buf.append(l)
        m = re.search(r"(?<![\w.])(\d{1,2}(?:\s*,\s*\d{1,2})*)\s*$", l)
        if m:
            us = [int(x) for x in re.findall(r"\d+", m.group(1)) if 1 <= int(x) <= 70]
            IENTS.append((" ".join(buf), us)); buf = []
    for u in range(1, 71):
        L, R = 6 + 2 * u, 7 + 2 * u
        ents = [e for e, us in IENTS if u in us]
        with open(f"{od}/int_u{u:02d}.txt", "w", encoding="utf-8") as f:
            f.write(f"# English Phrasal Verbs in Use Intermediate (2nd ed.) – Unit {u} – trang sách {L - 2}-{R - 2} (PDF {L}-{R})\n")
            f.write("# CẢNH BÁO: text OCR từ bản scan – có thể sai chữ, mất chữ, trộn cột. Đối chiếu ảnh trang: python3 tools/page_img.py int %d\n" % u)
            f.write("### BOLD: (không có – bản scan không giữ định dạng in đậm; xem ảnh trang)\n")
            f.write("\n### LEFT PAGE (lý thuyết, OCR):\n" + page(L))
            f.write("\n\n### RIGHT PAGE (bài tập, OCR):\n" + page(R))
            f.write("\n\n### KEY (đáp án, OCR):\n" + ikey.get(u, "(không tách được – xem ảnh trang Key)"))
            f.write("\n\n### MINI DICTIONARY (dòng OCR kết thúc bằng số unit này – có thể thiếu/nhiễu):\n" + ("\n".join(ents) or "(trống)"))

if __name__ == "__main__":
    main(*sys.argv[1:4])
