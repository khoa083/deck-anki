#!/usr/bin/env python3
"""evu_kit – English Vocabulary in Use (6 sách) -> Anki. Kiến trúc theo epv_kit, schema theo 2 deck demo.

  python3 evu.py src BOOK U [U…]        trích nguồn (trang lý thuyết **in đậm**, bài tập, đáp án) -> src/
  python3 evu.py make BOOK U [U…]       compile data/ -> units/ + audio + check   (quy trình chuẩn mỗi unit)
  python3 evu.py check [BOOK [U…]]      kiểm units/ (lỗi + cảnh báo)
  python3 evu.py build BOOK             -> out/<Root>.apkg
  python3 evu.py verify BOOK            import lại apkg: đếm note/thẻ, render, audio, GUID trùng, cây deck
  python3 evu.py status                 tiến độ từng sách
BOOK: ele (Elementary), pre (Pre-int & Int), upp (Upper-int), adv (Advanced), bus (Business Int), gva (Grammar & Vocabulary for Advanced)
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
    if units: files = [f for f in files if int(f[-7:-5]) in units]
    seen = collections.defaultdict(dict)   # book -> (word,sense) -> unit
    for f in sorted(glob.glob(os.path.join(KIT, "units", "*_u*.json"))):
        u = json.load(open(f, encoding="utf-8"))
        for it in u["items"]: seen[u["book"]].setdefault((it["word"].lower(), it.get("sense", "").lower()), u["unit"])
    nerr = 0
    for f in files:
        u = json.load(open(f, encoding="utf-8")); b = u["book"]; E = BD.validate(u, os.path.basename(f), b); W = []
        for it in u["items"]:
            k = (it["word"].lower(), it.get("sense", "").lower())
            if seen[b].get(k, u["unit"]) < u["unit"]: W.append(f"{it['word']}: đã có thẻ ở unit {seen[b][k]} – chỉ giữ nếu nghĩa khác (đặt sense)")
            if len(strip(it["grammar_vi"]).split()) < 15: W.append(f"{it['word']}: grammar_vi ngắn")
            if re.search(r"[A-Za-z]{3,}", re.sub(r"<i>.*?</i>|<b>.*?</b>", "", it["def_vi"])) and not re.search(r"[ăâđêôơưáàảãạ]", it["def_vi"]):
                W.append(f"{it['word']}: def_vi có vẻ chưa dịch")
        kit = sum(1 for it in u["items"] if it.get("ex_kit"))
        print(f"  {os.path.basename(f)[:-5]}: {len(u['items'])} mục | {len(E)} LỖI | ví dụ kit đặt {kit}")
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
    aud, miss = 0, []
    for nid in col.find_notes('"note:(Vocab In Use) Nhìn từ đoán nghĩa"'):
        n = col.get_note(nid); logical[(strip(n.fields[0]).lower(), n.fields[11], strip(n.fields[1])[:60])] += 1
        m = re.search(r"\[sound:([^\]]+)\]", n.fields[10])
        if m and os.path.exists(os.path.join(col.media.dir(), m.group(1))): aud += 1
        else: miss.append(strip(n.fields[0]))
    print(f"{book}: notes {col.note_count()} | cards {col.card_count()} | bad renders {bad} | audio {aud}/{aud + len(miss)}"
          + (f" THIẾU {miss[:8]}" if miss else "") + f" | GUID trùng {sum(v - 1 for v in guids.values() if v > 1)}"
          + f" | note logic trùng {sum(v - 1 for v in logical.values() if v > 1)}")
    for k, v in sorted(cnt.items()): print(f"  {v:6d}  {k}")
    col.close()


def status():
    for b, info in BOOKS.items():
        have = sorted(int(f[-7:-5]) for f in glob.glob(os.path.join(KIT, "units", f"{b}_u*.json")))
        demo = set(info.get("demo_units", []))
        n = len(info["units"]); done = sorted(set(have) | demo)
        items = sum(len(json.load(open(f))["items"]) for f in glob.glob(os.path.join(KIT, "units", f"{b}_u*.json")))
        todo = [u for u in range(1, n + 1) if u not in done]
        print(f"{b}: {len(done)}/{n} unit ({items} mục mới; demo {sorted(demo) or '-'}). Còn: {todo[:15]}{' …' if len(todo) > 15 else ''}")


def main(a):
    if not a or a[0] in ("-h", "help"): print(__doc__); return
    cmd = a[0]
    if cmd == "src": sys.exit(run("extract_src.py", *a[1:]))
    if cmd == "make":
        r = run("compile.py", *a[1:])
        names = [f"{a[1]}_u{int(x):02d}" for x in a[2:]]
        run("make_audio.py", *names)
        sys.exit(check(a[1], [int(x) for x in a[2:]]) or r)
    if cmd == "audio": sys.exit(run("make_audio.py", *a[1:]))
    if cmd == "check": sys.exit(1 if check(a[1] if len(a) > 1 else None, [int(x) for x in a[2:]] or None) else 0)
    if cmd == "build": sys.exit(run("build_deck.py", *a[1:]))
    if cmd == "verify": return verify(a[1])
    if cmd == "status": return status()
    print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
