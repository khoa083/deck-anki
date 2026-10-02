"""Trích nguồn 1 unit: trang lý thuyết (**in đậm** giữ nguyên), trang bài tập, đáp án (Key to Exercises).
Dùng: python3 tools/extract_src.py BOOK U [U…] -> src/<book>_uNNN.txt
Font của PDF: '!' = glyph 'Th'/'th', ﬀ/ﬁ/ﬂ/ﬃ/ﬄ = ff/fi/fl/ffi/ffl -> sửa lại."""
import sys, os, re, json, pymupdf
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = json.load(open(os.path.join(KIT, "tools", "books.json"), encoding="utf-8"))
LIG = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl", " ": " "}
def fix(s):
    for a, b in LIG.items(): s = s.replace(a, b)
    s = re.sub(r"(?<![A-Za-z])!(?=[a-z])", "Th", s)          # !e -> The, !is -> This
    s = re.sub(r"(?<=[A-Za-z])!(?=[a-z]|\b)", "th", s)          # wi! -> with, bo!er -> bother
    return s
def lines(page):
    out = []
    for b in page.get_text("dict", sort=True)["blocks"]:
        for l in b.get("lines", []):
            s = ""
            for sp in l["spans"]:
                t = fix(sp["text"]); isb = bool((sp["flags"] & 16) or re.search(r"Bold|Semibold|Black|Heavy", sp["font"]))
                s += (t[:len(t) - len(t.lstrip())] + "**" + t.strip() + "**" + (" " if t.endswith(" ") else "")) if isb and t.strip() else t
            s = re.sub(r"\*\*\s*\*\*", " ", s); s = re.sub(r"\s+", " ", s).strip()
            if s: out.append(s)
    return out
def key(d, book, u):
    toc = d.get_toc(); start = next(p - 1 for _, t, p in toc if t.strip().startswith("Key to Exercises"))
    end = next((p - 1 for _, t, p in toc if p - 1 > start), len(d))
    txt = "\n".join(fix(d[i].get_text()) for i in range(start, end))
    m = re.search(rf"(?m)^\s*{u}\.1\b.*?(?=^\s*{u + 1}\.1\b|^\s*UNIT {u + 1}\b|\Z)", txt, re.S)
    return m.group(0).strip() if m else ""
def main():
    book = sys.argv[1]; d = pymupdf.open(os.path.join(KIT, "books", f"{book}.pdf"))
    for u in map(int, sys.argv[2:]):
        info = BOOKS[book]["units"][str(u)]; p = info["page"] - 1
        txt = [f"### UNIT {u}: {info['title']} (PDF trang {p + 1}–{p + 2})", "### THEORY"] + lines(d[p]) + ["### EXERCISES"] + lines(d[p + 1]) + ["### KEY", key(d, book, u)]
        open(os.path.join(KIT, "src", f"{book}_u{u:03d}.txt"), "w", encoding="utf-8").write("\n".join(txt) + "\n")
if __name__ == "__main__": main()
