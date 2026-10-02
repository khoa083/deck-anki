#!/usr/bin/env python3
"""Công cụ điều phối kit English Phrasal Verbs in Use.

  python3 epv.py selftest               kiểm lại kit so với sách (tên unit, src, ánh xạ demo→bản 2)
  python3 epv.py doctor                 kiểm tra môi trường (anki, pymupdf, base, src, books)
  python3 epv.py status                 tiến độ: unit nào đã có (demo / units/*.json / còn thiếu)
  python3 epv.py check adv_u16 [...]    validate + tự sinh bảng tóm tắt + đối chiếu sách + lint (LỖI phải sửa hết)
  python3 epv.py demo adv 16            in thẻ demo mẫu (gold standard về văn phong) – mặc định 3 thẻ đầu unit
  python3 epv.py build                  build out/EPV_full.apkg từ base/ + units/
  python3 epv.py verify                 import thử vào collection trống: đếm note/thẻ, cây deck, render
"""
import sys, os, re, json, glob, html, collections, subprocess
KIT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(KIT, "tools"))
import build_deck as BD
BASE = glob.glob(os.path.join(KIT, "base", "*.apkg"))
OUT = os.path.join(KIT, "out", "EPV_full.apkg")
STOP = set("the a an and or of to in on at for with from into onto by as is be are was were been it its this that sb sth somebody something someone one’s one's oneself your his her their my".split())
PARTICLES = set("up down in out on off over back away about around round along across through by for with into onto after apart ahead aside forward together under without behind past".split())

def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
def toks(s): return re.findall(r"[a-z]+", s.lower().replace("’", "'").replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff"))

# ------------------------------------------------------------------ summary table (tự sinh)
SUM_RE = re.compile(r'\s*<hr>\s*<p><b>Phrasal verb summary</b>.*$', re.S)
def summary(items):
    rows = "".join(f"<tr><td><b>{it['word']}</b></td><td>{it['gloss_vi']}</td><td>{it['example']['en']}<br><i>{it['example']['vi']}</i></td></tr>" for it in items)
    return ('<hr> <p><b>Phrasal verb summary</b></p> <p><i>Tóm tắt phrasal verb trong bài</i></p> '
            f'<table><thead><tr><th>Phrasal verb</th><th>Nghĩa</th><th>Example / Ví dụ</th></tr></thead><tbody>{rows}</tbody></table>')

# ------------------------------------------------------------------ demo notes
_demo = None
def demo_notes():
    global _demo
    if _demo is None:
        import zipfile, sqlite3, tempfile
        d = tempfile.mkdtemp(); z = zipfile.ZipFile(BASE[0]); z.extract("collection.anki21", d)
        db = sqlite3.connect(os.path.join(d, "collection.anki21"))
        models = json.loads(db.execute("select models from col").fetchone()[0])
        vid = [int(k) for k, m in models.items() if m["name"] == BD.VOCAB_MODEL][0]
        _demo = []
        for (flds,) in db.execute("select flds from notes where mid=?", (vid,)):
            f = flds.split("\x1f"); n = int(f[10]) if f[10].isdigit() else 0
            _demo.append({"word": strip(f[0]), "demo_unit": n, "unit": None if n in BD.DEMO_EXTRA else BD.DEMO_RENUMBER.get(n, n), "fields": f})
    return _demo

def src(book, unit):
    p = os.path.join(KIT, "src", f"{book}_u{unit:02d}.txt")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

def in_source(word, S):
    miss = []
    for t in toks(re.sub(r"\([^)]*\)", "", word)):
        if t in STOP or len(t) < 2: continue
        cands = {t, t + "s", t + "es", t + "ed", t + "d", t + "ing", t[:-1] + "ing" if t.endswith("e") else t, t[:-1] + "ied" if t.endswith("y") else t,
                 t + t[-1] + "ed", t + t[-1] + "ing"}      # phụ âm nhân đôi: drop → dropped, dropping
        if not (cands & S) and not any(x.startswith(t[:max(4, len(t) - 2)]) for x in S if len(t) >= 5): miss.append(t)
    return miss

def ex_in_book(ex, text):
    e = toks(strip(ex)); T = " " + " ".join(toks(text)) + " "
    if not e: return 1.0
    if " " + " ".join(e) + " " in T: return 1.0
    best, n = 0, len(e)
    for k in range(n, 2, -1):          # dài nhất đoạn con liên tiếp khớp
        for i in range(0, n - k + 1):
            if " " + " ".join(e[i:i + k]) + " " in T: best = max(best, k / n); break
        if best: break
    return best

def longest_run(a, text):
    """Đoạn dài nhất (số từ) của a xuất hiện liên tiếp trong text."""
    A = toks(a); T = " " + " ".join(toks(text)) + " "; best = 0; i = 0
    while i < len(A):
        k = best + 1
        while i + k <= len(A) and " " + " ".join(A[i:i + k]) + " " in T: best = k; k += 1
        i += 1
    return best

V = "aeiouæʌɑɒɔəɜɪʊː"
def ipa_issues(ipa):
    out = []
    if re.search(r"oʊ|ɛ|ɹ|ɚ|ɝ|ɾ", ipa): out.append("ký hiệu kiểu Mỹ (oʊ/ɛ/ɹ/ɚ/ɝ/ɾ) – dùng chuẩn Anh (əʊ, e, r, ə, ɜː)")
    if re.search(r"ɑ(?!ː)", ipa): out.append("'ɑ' không có ː – chuẩn Anh dùng ɒ (hot) hoặc ɑː (car)")
    for w in ipa.strip("/").split():
        if re.search(rf"[{V}]r(?=[^{V}ˈˌ])", w): out.append(f"'r' sau nguyên âm trước phụ âm trong '{w}' (chuẩn Anh không phát âm)"); break
    return out

def vi_issues(label, s):
    out = []
    t = strip(s)
    if re.search(r"(^|[.!?]\s)Nó\b", t): out.append(f"{label}: câu mở đầu bằng 'Nó' – thường nên nêu rõ chủ ngữ")
    if "  " in s: out.append(f"{label}: có 2 dấu cách liền nhau")
    if re.search(r"\b(the|and|of|with|which|that)\b", strip(re.sub(r"<(b|i)>.*?</\1>", "", s))) and label != "example.vi":
        out.append(f"{label}: còn từ tiếng Anh ngoài <i>/<b> – kiểm tra đã dịch hết chưa")
    return out

def check(names):
    total_err = 0
    demo = demo_notes()
    for name in names:
        fp = os.path.join(KIT, "units", name + ".json")
        if not os.path.exists(fp): print(f"  {name}: KHÔNG CÓ FILE"); total_err += 1; continue
        u = json.load(open(fp, encoding="utf-8"))
        body = SUM_RE.sub("", u["theory_html"]).rstrip()
        u["theory_html"] = body + " " + summary(u["items"])
        json.dump(u, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        E = [e.split(": ", 1)[1] for e in BD.validate(u, name)]; W = []
        text = src(u["book"], u["unit"]); S = set(toks(text))
        run = longest_run(strip(body), text)
        if run >= 12: W.append(f"theory_html có đoạn {run} từ liên tiếp trùng sách – tóm tắt bằng lời mình (STYLE_GUIDE §3)")
        S |= {a + b for a, b in zip(toks(text), toks(text)[1:])}
        NS = [0, 0]
        md = re.search(r"### MINI DICTIONARY.*?\n(.*)", text, re.S); md = md.group(1) if md else ""
        for it in u["items"]:
            w = it["word"]
            m = in_source(w, S)
            if m: E.append(f"{w}: từ {m} KHÔNG có trong trang sách của unit – headword phải lấy từ sách")
            r = ex_in_book(it["example"]["en"], text)
            if r >= 0.6 and len(toks(strip(it["example"]["en"]))) >= 5: W.append(f"{w}: ví dụ trùng câu sách ({r:.0%}) – viết câu riêng (chế độ tóm tắt, xem STYLE_GUIDE §0)")
            r2 = ex_in_book(it["def_en"], text)
            if r2 >= 0.7 and len(toks(it["def_en"])) >= 8: W.append(f"{w}: def_en gần như chép Mini dictionary ({r2:.0%}) – viết lại bằng lời mình")
            E += [f"{w}: IPA {x}" for x in ipa_issues(it["ipa"])]
            n = len(strip(it["grammar_vi"]).split())
            if not 80 <= n <= 240: E.append(f"{w}: grammar_vi {n} từ (cần 80–240, như demo)")
            if len(it["gloss_vi"].split()) > 8: W.append(f"{w}: gloss_vi dài ({len(it['gloss_vi'].split())} từ) – nên ≤ 8")
            if not it["def_en"].rstrip().endswith("."): E.append(f"{w}: def_en phải kết thúc bằng dấu chấm (như demo)")
            if not it["def_vi"].rstrip().endswith("."): E.append(f"{w}: def_vi phải kết thúc bằng dấu chấm (như demo)")
            for lab, v in (("def_vi", it["def_vi"]), ("grammar_vi", it["grammar_vi"])): W += [f"{w}: {x}" for x in vi_issues(lab, v)]
            # bám sách: mọi chunk <i>…</i> trong phần Collocations phải có trong src của unit
            cm = re.search(r"<b>Collocations / chunks</b>:(.*?)<b>Register</b>", it["grammar_vi"], re.S)
            for ch in re.findall(r"<i>(.*?)</i>", cm.group(1) if cm else ""):
                miss = in_source(re.sub(r"\b(somebody|something|someone|sb|sth|your|you|has|have|had|is|are|was|were|will|be|been|his|her|their|them|him|me|my|our|us|we|it)\b", "", ch), S)
                if miss: W.append(f"{w}: collocation '{ch}' có từ {miss} không có trong src unit – chỉ dùng collocation của sách")
            for rel_ in it["synonyms"] + it["antonyms"]:
                if in_source(rel_["text"], S): NS[0] += 1
                NS[1] += 1
            if "sách" in re.sub(r"(chính|ngân|danh|giá|tủ|hiệu) sách|sách đọc|sách luật", "", it["grammar_vi"].lower()): W.append(f"{w}: grammar_vi nói 'sách…' – chắc chắn điều đó CÓ trong sách (xem src)")
            if u["book"] == "adv":
                for d in demo:
                    if d["word"].lower() == w.lower(): W.append(f"{w}: đã có trong demo (unit {d['unit']}) – chỉ giữ nếu là nghĩa khác, đặt 'sense'")
        # độ phủ Mini dictionary
        words = [it["word"] for it in u["items"]]
        if u["book"] == "adv": words += [d["word"] for d in demo if d["unit"] == u["unit"]]   # unit demo: tính cả thẻ demo
        heads = " ".join(toks(" ".join(words)))
        miss = []
        for line in md.splitlines():
            h = re.split(r" — | (?=to |if |when |used )", line.lstrip("- "), 1)[0]
            core = [t for t in toks(h) if t not in STOP and t != "or"][:3]
            if core and not all(re.search(rf"\b{re.escape(c[:4])}", heads) for c in core[:2]): miss.append(h.strip()[:50])
        if miss: W.append(f"Mini dictionary có {len(miss)} mục chưa có thẻ: " + "; ".join(miss[:12]) + (" …" if len(miss) > 12 else ""))
        # trùng trong cả sách
        allw = collections.Counter()
        for f in glob.glob(os.path.join(KIT, "units", f"{u['book']}_u*.json")):
            for it in json.load(open(f, encoding="utf-8"))["items"]: allw[(it["word"].lower(), it.get("sense", "").lower())] += 1
        for it in u["items"]:
            if allw[(it["word"].lower(), it.get("sense", "").lower())] > 1: W.append(f"{it['word']}: trùng word+sense với unit khác cùng sách")
        W.append(f"(thông tin) đồng/trái nghĩa không có trong src: {NS[0]}/{NS[1]} – ưu tiên cụm của unit/định nghĩa sách")
        total_err += len(E)
        print(f"  {name}: {len(u['items'])} mục | {len(E)} LỖI | {len(W)} cảnh báo")
        for e in E: print("   LỖI  ", e)
        for w_ in W: print("   warn ", w_)
    print(f"{len(names)} unit, {'0 LỖI – có thể build.' if not total_err else str(total_err) + ' LỖI – sửa rồi chạy lại check.'}")
    return total_err

def status():
    done = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(KIT, "units", "*.json"))}
    dm = sorted({d["unit"] for d in demo_notes() if d["unit"]})
    print("Demo (Advanced, đã đánh số lại theo bản 2):", dm, "+ unit bổ sung 'New phrasal verbs' (bản 1)")
    for b, n in (("adv", 60), ("int", 70)):
        have = [u for u in range(1, n + 1) if f"{b}_u{u:02d}" in done or (b == "adv" and u in dm)]
        todo = [u for u in range(1, n + 1) if u not in have]
        print(f"{b}: {len(have)}/{n} unit có. Còn thiếu: {todo[:12]}{' …' if len(todo) > 12 else ''}")

def show_demo(book, unit, k=3):
    for d in [d for d in demo_notes() if d["unit"] == unit][:k]:
        names = ["Từ vựng", "Định nghĩa (a)", "IPA", "Định nghĩa (v)", "Dịch nghĩa", "Câu ví dụ", "Dịch câu ví dụ", "Trái nghĩa", "Đồng nghĩa", "Ngữ pháp", "STT"]
        print("=" * 60)
        for n_, f in zip(names, d["fields"]): print(f"[{n_}] {f}")

def selftest():
    """Kiểm lại các điều kit khẳng định về sách (chạy khi bắt đầu chat mới)."""
    import pymupdf
    ok = True
    def norm(x): return re.sub(r"[^a-z]", "", x.lower())
    pdf = os.path.join(KIT, "books", "adv.pdf")
    if os.path.exists(pdf):
        d = pymupdf.open(pdf)
        bad = [u for u, (en, vi) in BD.BOOKS["adv"]["units"].items() if norm(en) not in norm(d[7 + 2 * int(u)].get_text()[:300])]
        print("Advanced: tên unit khớp trang sách:", 60 - len(bad), "/ 60", bad or ""); ok &= not bad
    else: print("Advanced: chưa có books/adv.pdf – bỏ qua"); ok = False
    miss = [f for f in (f"{b}_u{u:02d}" for b, n in (("adv", 60), ("int", 70)) for u in range(1, n + 1)) if not src(f[:3], int(f[5:]))]
    print("src: thiếu", miss or "0 file"); ok &= not miss
    weak = [f"int{u}" for u, (en, vi) in BD.BOOKS["int"]["units"].items() if norm(en)[:10] not in norm(src("int", int(u))[:900])]
    print("Intermediate: tiêu đề OCR không đọc rõ ở", len(weak), "unit (đã kiểm bằng ảnh khi làm kit, xem implementation-notes):", weak)
    for du, nu in list(BD.DEMO_RENUMBER.items())[:2]:
        C = set(w for d_ in demo_notes() if d_["demo_unit"] == du for w in toks(d_["word"]))
        print(f"demo unit {du} -> bản 2 unit {nu}: {len(C & set(toks(src('adv', nu))))}/{len(C)} từ của headword có trên trang sách")
    print("SELFTEST", "OK" if ok else "CÓ VẤN ĐỀ")

def verify():
    import tempfile
    from anki.collection import Collection, ImportAnkiPackageRequest, ImportAnkiPackageOptions
    d = tempfile.mkdtemp(); col = Collection(os.path.join(d, "t.anki2"))
    r = col.import_anki_package(ImportAnkiPackageRequest(package_path=OUT, options=ImportAnkiPackageOptions(with_scheduling=True, with_deck_configs=True)))
    cnt = collections.Counter(); bad = 0
    for cid in col.find_cards(""):
        c = col.get_card(cid); cnt["::".join(col.decks.name(c.did).split("::")[:3])] += 1
        try:
            q, a = c.question(), c.answer()
            if "{{" in a or "Unknown field" in a: bad += 1
        except Exception: bad += 1
    print("notes:", col.note_count(), "cards:", col.card_count(), "bad renders:", bad)
    nids = col.find_notes("(tag:EPV::adv::u* OR tag:EPV::int::u*)"); aud = 0; miss = []
    for nid in nids:
        n = col.get_note(nid)
        if len(n.fields) > 11:
            m_ = re.search(r"\[sound:([^\]]+)\]", n.fields[11])
            if m_ and os.path.exists(os.path.join(col.media.dir(), m_.group(1))): aud += 1
            else: miss.append(strip(n.fields[0]))
    print(f"audio thẻ mới: {aud}/{aud + len(miss)}" + (f" – THIẾU: {miss[:10]}" if miss else " – đủ"))
    for k, v in sorted(cnt.items()): print(f"  {v:5d}  {k}")
    from nobrand import brand_left
    print("còn chữ Anki Support Vietnam:", brand_left(col))
    print("top decks:", sorted({n.name.split('::')[0] for n in col.decks.all_names_and_ids()}))
    col.close()

if __name__ == "__main__":
    a = sys.argv[1:] or ["status"]
    if a[0] == "doctor":
        import shutil; print("ffmpeg:", "OK" if shutil.which("ffmpeg") else "THIẾU (apt install ffmpeg)")
        print("model TTS:", "OK" if os.path.exists(os.path.expanduser("~/.cache/epv_tts/kokoro-v1.0.onnx")) else "chưa tải – `epv.py audio` tự tải từ GitHub")
        for m in ("anki", "pymupdf", "kokoro_onnx", "soundfile"):
            try: __import__(m); print("OK", m)
            except ImportError: print("THIẾU", m, "-> pip install", m, "--break-system-packages")
        print("base:", BASE); print("src:", len(glob.glob(os.path.join(KIT, "src", "*.txt"))), "file (cần 130)")
        print("books/:", os.listdir(os.path.join(KIT, "books")) if os.path.isdir(os.path.join(KIT, "books")) else "CHƯA CÓ – copy 2 PDF vào books/adv.pdf, books/int.pdf")
    elif a[0] == "status": status()
    elif a[0] == "check": sys.exit(1 if check([x.replace(".json", "") for x in a[1:]]) else 0)
    elif a[0] == "demo": show_demo(a[1], int(a[2]), int(a[3]) if len(a) > 3 else 3)
    elif a[0] == "build":
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        sys.exit(subprocess.call([sys.executable, os.path.join(KIT, "tools", "build_deck.py"), BASE[0], os.path.join(KIT, "units"), OUT]))
    elif a[0] == "audio": sys.exit(subprocess.call([sys.executable, os.path.join(KIT, "tools", "make_audio.py")] + a[1:]))
    elif a[0] == "verify": verify()
    elif a[0] == "selftest": selftest()
    else: print(__doc__)
