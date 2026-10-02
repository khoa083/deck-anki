"""Trích nguồn 1 unit: trang trái (lý thuyết, **in đậm**), trang phải (bài tập), đáp án.
Dùng: python3 tools/extract_src.py BOOK UNIT [UNIT2 ...]  → src/<book>_uNN.txt
PDF mất glyph ghép (fi/fl/ff/ffi/ffl) → sửa bằng tần suất từ (wordfreq); mọi chỗ sửa ghi ở dòng '### LIGATURE'."""
import sys, os, re, json, pymupdf
from wordfreq import zipf_frequency as Z
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = json.load(open(os.path.join(KIT, "tools", "books.json"), encoding="utf-8"))
LIG = ["fi", "fl", "ff", "ffi", "ffl"]
_cache = {}
def fix_word(w, log):
    lw = w.lower()
    if lw in _cache: r = _cache[lw]
    else:
        z0 = Z(lw, "en"); best = (z0 + 2.0, None)
        if z0 < 3.0 and len(lw) >= 2:
            for i in range(len(lw) + 1):
                for g in LIG:
                    c = lw[:i] + g + lw[i:]; zc = Z(c, "en")
                    if zc >= 3.2 and zc > best[0]: best = (zc, c)
        r = _cache[lw] = best[1]
    if not r: return w
    log.add(f"{w}->{r}")
    return r.capitalize() if w[:1].isupper() else r
def fix_text(s, log):
    return re.sub(r"[A-Za-z]+", lambda m: fix_word(m.group(0), log), s)
def page_lines(page, log, bold=True):
    """Dựng dòng từ glyph (rawdict): chèn dấu cách khi khoảng trống giữa 2 glyph > 0.08×cỡ chữ (PDF Elementary không có ký tự cách)."""
    out = []
    for b in page.get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            s, prev = "", None
            for sp in l["spans"]:
                isb = bool((sp["flags"] & 16) or re.search(r"Bold|Semibold|Black|Heavy", sp["font"]))
                t = ""
                for c in sp["chars"]:
                    if prev is not None and c["c"] != " " and not t.endswith(" ") and not (s + t).endswith(" "):
                        gap = c["bbox"][0] - prev["bbox"][2]
                        if gap > 0.08 * sp["size"]: t += " "
                    t += c["c"]; prev = c
                t = fix_text(t, log)
                if bold and isb and t.strip():
                    lead = t[:len(t) - len(t.lstrip())]; s += lead + "**" + t.strip() + "**" + (" " if t.endswith(" ") else "")
                else: s += t
            s = re.sub(r"\*\*\s*\*\*", " ", s).strip(); s = re.sub(r"  +", " ", s)
            if s and s != "Audio not supported": out.append(s)
    return out
def key_text(d, book, unit, log):
    toc = d.get_toc(); start = next((p - 1 for _, t, p in toc if t.strip().lower().startswith("answer key")), None)
    if start is None: return ""
    txt = "\n".join(fix_text(d[i].get_text(), log) for i in range(start, min(start + 60, len(d))))
    m = re.search(rf"(?m)^\s*{unit}\.\d\b.*?(?=^\s*{unit + 1}\.\d\b|\Z)", txt, re.S)
    return m.group(0).strip()[:5000] if m else ""
def main():
    book = sys.argv[1]; d = pymupdf.open(os.path.join(KIT, "books", f"{book}.pdf"))
    for u in map(int, sys.argv[2:]):
        info = BOOKS[book]["units"][str(u)]; p = info["page"]; log = set()
        n = info.get("npages", 2)
        if "npages" in info:   # sách scan OCR (gva): không có thông tin in đậm; cả unit nhiều trang -> LEFT
            left = sum(([f"### PAGE {i + 1}"] + [l.strip() for l in d[i].get_text().splitlines() if l.strip()] for i in range(p, p + n)), []); right = []
        else:
            left = page_lines(d[p], log); right = page_lines(d[p + 1], log, bold=False)
        key = key_text(d, book, u, log)
        s = (f"### UNIT {u}: {info['en']} (PDF trang {p + 1}–{p + n})\n### LIGATURE: {', '.join(sorted(log)) or '-'}\n"
             f"### LEFT\n" + "\n".join(left) + "\n### RIGHT\n" + "\n".join(right) + "\n### KEY\n" + key + "\n")
        open(os.path.join(KIT, "src", f"{book}_u{u:02d}.txt"), "w", encoding="utf-8").write(s)
        print(f"src/{book}_u{u:02d}.txt", len(s), "ligature:", len(log))
main()
