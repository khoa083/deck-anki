#!/usr/bin/env python3
"""egu_kit – Grammar in Use (Essential, Advanced) -> Anki. Kiến trúc theo epv_kit/evu_kit, schema theo deck mẫu
English Grammar In Use (Intermediate).apkg.

  python3 egu.py src                    trích nguồn (lý thuyết **in đậm**, bài tập, đáp án) -> src/
  python3 egu.py make BOOK U [U…]       compile data/ -> units/ + check   (quy trình chuẩn mỗi unit)
  python3 egu.py check [BOOK [U…]]      kiểm units/ (lỗi + cảnh báo)
  python3 egu.py build BOOK             -> out/<Root>.apkg
  python3 egu.py verify BOOK            import lại apkg: đếm note/thẻ, render, GUID trùng, cây deck
  python3 egu.py status                 tiến độ từng sách
BOOK: ess (Essential Grammar in Use, 4th ed.), agu (Advanced Grammar in Use, 3rd ed.)
"""
import sys, os, re, json, glob, subprocess, collections, html
KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(KIT, "tools"))
BOOKS = json.load(open(os.path.join(KIT, "tools", "books.json"), encoding="utf-8"))
PY = sys.executable


def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def run(*a): return subprocess.call([PY] + [os.path.join(KIT, "tools", a[0])] + list(a[1:]))


def check(book=None, units=None):
    import build_deck as BD
    files = sorted(glob.glob(os.path.join(KIT, "units", f"{book or '*'}_u*.json")))
    if units: files = [f for f in files if int(re.search(r'_u(\d+)\.json$', f).group(1)) in units]
    nerr = 0
    for f in files:
        u = json.load(open(f, encoding="utf-8")); E = BD.validate(u, os.path.basename(f), u["book"]); W = []
        opts = collections.Counter(q["a"] for q in u["mcq"])
        for q in u["mcq"]:
            if not re.search(r"[À-ỹđĐ]", q["vi"]): W.append(f"'{strip(q['question'])[:40]}': bản dịch có vẻ chưa dịch")
        qs = collections.Counter(strip(q["question"]).lower() for q in u["mcq"])
        W += [f"câu hỏi lặp {v} lần: {k[:50]}" for k, v in qs.items() if v > 1]
        print(f"  {os.path.basename(f)[:-5]}: {len(u['mcq'])} MCQ | {len(E)} LỖI | đáp án hay gặp nhất: {opts.most_common(1)}")
        for e in E: print("   LỖI ", e)
        for w in W: print("   warn ", w)
        nerr += len(E)
    print(f"{len(files)} unit, {nerr} LỖI")
    return nerr


def verify(book):
    import tempfile
    from anki.collection import Collection, ImportAnkiPackageRequest, ImportAnkiPackageOptions
    out = os.path.join(KIT, "out", BOOKS[book]["root"] + ".apkg")
    d = tempfile.mkdtemp(); col = Collection(os.path.join(d, "t.anki2"))
    col.import_anki_package(ImportAnkiPackageRequest(package_path=out, options=ImportAnkiPackageOptions(with_scheduling=True, with_deck_configs=True)))
    cnt = collections.Counter(); bad = 0
    for cid in col.find_cards(""):
        c = col.get_card(cid); cnt["::".join(col.decks.name(c.did).split("::")[:2])] += 1
        try:
            q, a = c.question(), c.answer()
            if "{{" in q + a or "Unknown field" in q + a or not strip(q): bad += 1
        except Exception: bad += 1
    nids = col.find_notes(""); guids = collections.Counter(col.get_note(n).guid for n in nids)
    logical = collections.Counter()
    for nid in col.find_notes('"note:MCQ custom shuffled (Grammar)"'):
        n = col.get_note(nid); logical[(strip(n["Question"]).lower(), strip(n["a"]).lower())] += 1
    units = len({col.decks.name(col.get_card(c).did) for c in col.find_cards('"note:MCQ custom shuffled (Grammar)"')})
    print(f"{book}: notes {col.note_count()} | cards {col.card_count()} | unit có MCQ {units} | bad renders {bad}"
          + f" | GUID trùng {sum(v - 1 for v in guids.values() if v > 1)} | MCQ logic trùng {sum(v - 1 for v in logical.values() if v > 1)}"
          + f" | note type {[m['name'] for m in col.models.all()]}")
    for k, v in sorted(cnt.items()): print(f"  {v:6d}  {k}")
    col.close()


def status():
    for b, info in BOOKS.items():
        have = sorted(int(re.search(r'_u(\d+)\.json$', f).group(1)) for f in glob.glob(os.path.join(KIT, "units", f"{b}_u*.json")))
        n = len(info["units"]); mcq = sum(len(json.load(open(f))["mcq"]) for f in glob.glob(os.path.join(KIT, "units", f"{b}_u*.json")))
        apps = len(glob.glob(os.path.join(KIT, "units", f"{b}_a*.json")))
        todo = [u for u in range(1, n + 1) if u not in have]
        print(f"{b}: {len(have)}/{n} unit, {mcq} MCQ, {apps}/{len(info.get('appendices', []))} phụ lục. Còn: {todo[:15]}{' …' if len(todo) > 15 else ''}")


def main(a):
    if not a or a[0] in ("-h", "help"): print(__doc__); return
    cmd = a[0]
    if cmd == "src": sys.exit(run("extract_src.py", *a[1:]))
    if cmd == "make":
        r = run("compile.py", *a[1:])
        sys.exit(check(a[1], [int(x) for x in a[2:]] or None) or r)
    if cmd == "check": sys.exit(1 if check(a[1] if len(a) > 1 else None, [int(x) for x in a[2:]] or None) else 0)
    if cmd == "build": sys.exit(run("build_deck.py", *a[1:]))
    if cmd == "verify": return verify(a[1])
    if cmd == "status": return status()
    print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
