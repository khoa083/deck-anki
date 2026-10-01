#!/usr/bin/env python3
"""Build deck English Phrasal Verbs in Use (Advanced + Intermediate) từ deck demo + units/*.json.

Dùng:  python3 tools/build_deck.py BASE.apkg UNITS_DIR OUT.apkg [--check-only]

Cách làm (dùng API chính thức của thư viện `anki`, không sửa SQL tay):
 1. Import deck demo (base/) vào một collection trống.
 2. Đổi cấu trúc deck: "English Phrasal Verbs in Use (Advanced)" -> "English Phrasal Verbs in Use::Advanced".
 3. Đánh số lại unit của demo theo SÁCH BẢN 2 (PDF): demo theo bản 1 có unit 9 "New phrasal verbs"
    (bản 2 không có) và unit 10-16 = bản 2 unit 9-15. Xem DEMO_RENUMBER.
 4. Chuẩn hoá note demo: nhãn từ loại (noun -> n., adjective -> adj.), IPA sang chuẩn Anh (config.ipa_style).
 5. Thay note Mục lục (00-Contents) bằng mục lục bản 2 (giữ GUID), thêm mục lục Intermediate.
 6. Thêm note từ units/*.json (GUID cố định theo sách|unit|word|sense -> import lại chỉ cập nhật).
 7. Xuất .apkg (kèm media của demo).
Chạy lại nhiều lần an toàn: luôn build lại từ deck demo gốc.
"""
import sys, os, re, json, hashlib, tempfile, html

HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from make_audio import audio_name          # media/epv_<book>_u<NN>_<slug>.mp3 – BẮT BUỘC mỗi mục có audio
BOOKS = json.load(open(os.path.join(HERE, "books.json"), encoding="utf-8"))
CFG = json.load(open(os.path.join(KIT, "config.json"), encoding="utf-8"))
VOCAB_MODEL = "(Phrasal verb In Use) Nhìn từ đoán nghĩa"
THEORY_MODEL = "Tóm tắt"
SOURCE = "AnkiSupportVietnam"
ROOT = "English Phrasal Verbs in Use"
OLD_TOP = {"English Phrasal Verbs in Use (Advanced)": "Advanced", "English Phrasal Verbs in Use (Intermediate)": "Intermediate"}
V_THEORY, V_LOOK, V_LISTEN = "Lý thuyết", "Từ vựng (nhìn từ, gõ nghĩa)", "Từ vựng (nghe, gõ từ đúng)"
HR = '<hr style="border: none; height: 0.5px; background-color: #e0e0e0;">'
# demo (bản 1) -> sách PDF (bản 2). Unit 9 "New phrasal verbs" chỉ có ở bản 1: giữ lại làm bài bổ sung.
DEMO_RENUMBER = {10: 9, 11: 10, 12: 11, 13: 12, 14: 13, 15: 14, 16: 15}
DEMO_EXTRA = {9: "08x-New phrasal verbs (bổ sung, chỉ có ở bản 1)"}
# Sửa note demo đã kiểm với sách bản 2 (xem implementation-notes.md, mục Rà soát demo):
DEMO_WORD_FIX = {"hit upon": "hit on", "bear upon": "bear on", "call upon": "call on"}      # sách bản 2 dùng dạng 'on'
DEMO_ED1_ONLY = {("flirt with somebody", 5), ("flirt with something", 5), ("wake up and smell the coffee", 8), ("wake up", 15)}  # số unit của demo (bản 1)
BATH = r"\b(ask|asks|asking|after|pass|passed|past|branch|dance|chance|plant|staff|laugh|path|grass|fast|last|class|glass|answer|advance|demand|example|master|vast|draft|craft)\b"
POS_OK = {"phr.v.", "n.", "adj.", "idiom", "phrase", "v."}
POS_FIX = {"noun": "n.", "adjective": "adj.", "expression": "phrase", "phrasal verb": "phr.v."}


def strip_html(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def curly(s):
    return "".join(p if p.startswith("<") else p.replace("'", "’") for p in re.split(r"(<[^>]+>)", s))


def guid_for(*parts):
    h = hashlib.sha1("|".join(map(str, parts)).encode("utf-8")).digest()
    a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./:;<=>?@[]^_`{|}~"
    n = int.from_bytes(h[:8], "big"); out = ""
    while n: n, r = divmod(n, len(a)); out += a[r]
    return "epv" + out


def section_of(book, unit):
    for a, b, name in BOOKS[book]["sections"]:
        if a <= unit <= b: return name
    raise ValueError(f"unit {unit} ngoài phạm vi sách {book}")


def unit_title(book, unit):
    return BOOKS[book]["units"][str(unit)]


def unit_deck(book, unit):
    en, _ = unit_title(book, unit)
    return f"{unit:02d}-{en}"


def tag_balance_errors(s):
    errs = []
    for t in ("b", "i", "p", "div", "table", "tr", "td", "th", "ul", "li", "thead", "tbody", "span"):
        o = len(re.findall(rf"<{t}(\s[^>]*)?>", s)); c = len(re.findall(rf"</{t}>", s))
        if o != c: errs.append(f"thẻ <{t}> mở {o} / đóng {c}")
    return errs


V = "aeiouæʌɑɒɔəɜɪʊɛː"
def uk_ipa(ipa):
    """Chuyển IPA kiểu Mỹ (như demo) sang chuẩn Anh. Không đụng tới IPA đã chuẩn Anh."""
    s = ipa.replace("oʊ", "əʊ").replace("ɛ", "e").replace("ɝ", "ɜː").replace("ɚ", "ə").replace("ɹ", "r")
    s = re.sub(r"ɑ(?!ː)r?", lambda m: "ɑː" if m.group(0) == "ɑr" else "ɒ", s)   # US ɑ (lot) -> ɒ ; ɑr -> ɑː
    s = re.sub(r"ɔ(?![ːɪ])(?=[fsŋgθ])", "ɒ", s)                              # US ɔ (off, long) -> ɒ
    s = re.sub(r"ɔ(?![ːɪ])", "ɔː", s)                                          # US ɔ (for, thought) -> ɔː
    out = []
    for w in s.split(" "):
        w = re.sub(rf"(?<=[{V}])r(?=[^{V}ˈˌ/]|/|$)", "", w)
        w = re.sub(rf"(?<=[{V}])r(?=[ˈˌ][^{V}])", "", w)
        out.append(w)
    return " ".join(out)


# ---------------------------------------------------------------- validation (dùng chung với epv.py)
def validate(u, fname):
    E = []
    book, unit = u.get("book"), u.get("unit")
    if book not in BOOKS: E.append("book phải là 'adv' hoặc 'int'")
    elif not isinstance(unit, int) or str(unit) not in BOOKS[book]["units"]: E.append("unit sai")
    body = u.get("theory_html", "")
    if u.get("supplement"):
        if book != "adv" or unit > 15: E.append("supplement chỉ dùng cho Advanced unit 1–15 (unit đã có trong demo)")
    else:
        if len(strip_html(body)) < 500: E.append("theory_html quá ngắn")
        if "Phrasal verb summary" not in body: E.append("theory_html thiếu bảng 'Phrasal verb summary' (chạy epv.py check để tự sinh)")
        if not re.search(r"<p><b>A\.", body): E.append("theory_html thiếu mục 'A.'")
        E += ["theory_html: " + e for e in tag_balance_errors(body)]
    items = u.get("items", [])
    if len(items) < (1 if u.get("supplement") else 5): E.append("quá ít mục")
    seen = set()
    for k, it in enumerate(items, 1):
        w = it.get("word", "").strip(); p = f"item #{k} '{w}'"
        key = (w.lower(), it.get("sense", "").strip().lower())
        if not w: E.append(f"{p}: thiếu word"); continue
        if book in BOOKS and isinstance(unit, int) and not os.path.exists(os.path.join(KIT, "media", audio_name(book, unit, it))):
            E.append(f"{p}: thiếu audio media/{audio_name(book, unit, it)} – chạy `python3 epv.py audio`")
        if key in seen: E.append(f"{p}: trùng (word+sense) – nếu là nghĩa khác, đặt 'sense' khác nhau")
        seen.add(key)
        for f in ("pos", "def_en", "ipa", "def_vi", "gloss_vi", "grammar_vi"):
            if not str(it.get(f, "")).strip(): E.append(f"{p}: thiếu {f}")
        if it.get("pos") not in POS_OK: E.append(f"{p}: pos phải thuộc {sorted(POS_OK)}")
        ipa = it.get("ipa", "")
        if ipa and not re.fullmatch(r"/[^/]+/", ipa): E.append(f"{p}: ipa phải dạng /.../")
        ex = it.get("example", {})
        if "<b>" not in ex.get("en", ""): E.append(f"{p}: example.en phải bôi đậm phrasal verb bằng <b>")
        if "<b>" not in ex.get("vi", ""): E.append(f"{p}: example.vi phải bôi đậm phần dịch tương ứng bằng <b>")
        for f in ("synonyms", "antonyms"):
            lst = it.get(f)
            if not isinstance(lst, list) or not lst: E.append(f"{p}: {f} phải là list ≥1"); continue
            for s in lst:
                if not all(str(s.get(x, "")).strip() for x in ("text", "pos", "vi")): E.append(f"{p}: {f} mỗi phần tử cần text/pos/vi")
        g = it.get("grammar_vi", "")
        for need in ("<b>Grammar</b>", "<b>Register</b>"):
            if need not in g: E.append(f"{p}: grammar_vi thiếu '{need}'")
        E += [f"{p}: grammar_vi " + e for e in tag_balance_errors(g)]
    return [f"{fname}: {e}" for e in E]


# ---------------------------------------------------------------- field composers
def theory_field(book, unit, body):
    en, vi = unit_title(book, unit)
    head = (f'<div style="text-align: center;"><span style="color: rgb(0, 107, 166);"><b>Unit {unit}: {en}</b></span>'
            f'<div><i>Bài {unit}: {vi}</i></div></div> {HR} ')
    body = (body.strip().replace("<hr>", HR)
            .replace("<table>", '<table border="1" style="border-collapse: collapse; border-color: black; width: 100%; text-align: left;">')
            .replace("<td>", '<td style="padding: 8px;">').replace("<th>", '<th style="padding: 8px;">'))
    return head + body


def rel(lst):
    return ", ".join(f'{s["text"]} <i>({s["pos"]} {s["vi"]})</i>' for s in lst)


def vocab_fields(u, it, theory):
    return [it["word"].strip(), f'<i>{it["pos"]}</i> {it["def_en"].strip()}', it["ipa"].strip(), it["def_vi"].strip(),
            it["gloss_vi"].strip(), it["example"]["en"].strip(), it["example"]["vi"].strip(), rel(it["antonyms"]),
            rel(it["synonyms"]), it["grammar_vi"].strip(), f'{u["unit"]:03d}', it.get("audio", ""), theory, SOURCE]


def toc_field(book):
    b = BOOKS[book]
    parts = ['<div style="text-align: center;"><b><font color="#006ba6">Contents</font></b><div><i>Mục lục</i></div></div> ' + HR]
    for a, z, name in b["sections"]:
        num, title = name.split("-", 1)
        vi = b.get("sections_vi", {}).get(name, "")
        parts.append(f"<p><b>{title}</b><br><i>{vi}</i></p> <ul>" + "".join(
            f'<li>{n}. {b["units"][str(n)][0]}<br><i>{b["units"][str(n)][1]}</i></li>' for n in range(a, z + 1)) + "</ul> " + HR)
    return " ".join(parts)


# ---------------------------------------------------------------- build
def main():
    if len(sys.argv) < 4: print(__doc__); sys.exit(1)
    base, udir, out = sys.argv[1:4]
    units, errs = [], []
    for fn in sorted(os.listdir(udir)):
        if not fn.endswith(".json"): continue
        try: u = json.load(open(os.path.join(udir, fn), encoding="utf-8"))
        except Exception as e: errs.append(f"{fn}: JSON lỗi: {e}"); continue
        errs += validate(u, fn); units.append(u)
    if errs: print("LỖI VALIDATE:\n  " + "\n  ".join(errs)); sys.exit(2)
    print(f"OK validate {len(units)} unit, {sum(len(u['items']) for u in units)} mục")
    if "--check-only" in sys.argv: return

    from anki.collection import Collection, ImportAnkiPackageRequest, ImportAnkiPackageOptions, ExportAnkiPackageOptions
    from anki.import_export_pb2 import ExportLimit
    from anki.generic_pb2 import Empty
    d = tempfile.mkdtemp(); col = Collection(os.path.join(d, "c.anki2"))
    col.import_anki_package(ImportAnkiPackageRequest(package_path=base, options=ImportAnkiPackageOptions(with_scheduling=False, with_deck_configs=True)))
    st = {"demo_notes_fixed": 0, "notes_added": 0, "decks_renamed": 0}
    vm, tm = col.models.by_name(VOCAB_MODEL), col.models.by_name(THEORY_MODEL)
    assert vm and tm, "không thấy note type của demo"

    # 2-3. đổi tên deck (con trước cha để tránh trùng tên), đánh số lại unit demo
    for nd in sorted(col.decks.all_names_and_ids(), key=lambda x: -x.name.count("::")):
        parts = nd.name.split("::"); new = list(parts)
        if parts[0] in OLD_TOP and len(parts) >= 4 and parts[-1][:2].isdigit():
            n = int(parts[-1][:2])
            if n in DEMO_RENUMBER:
                new[-1] = f"{DEMO_RENUMBER[n]:02d}-" + parts[-1].split("-", 1)[1]
            elif n in DEMO_EXTRA:
                new[-1] = DEMO_EXTRA[n]
        if new != parts:
            col.decks.rename(nd.id, "::".join(new)); st["decks_renamed"] += 1
    for nd in col.decks.all_names_and_ids():
        if nd.name in OLD_TOP:
            col.decks.rename(nd.id, f"{ROOT}::{OLD_TOP[nd.name]}"); st["decks_renamed"] += 1

    # 4. chuẩn hoá note demo (+ đánh số lại STT / tiêu đề Unit trong lý thuyết)
    def renum(text):
        if "New phrasal verbs" in text[:600]:      # bài bản 1: đánh dấu, không đổi số
            return re.sub(r"(>\s*)(Unit|Bài) 9:", r"\g<1>\2 9 (bản 1):", text)
        for old, new in sorted(DEMO_RENUMBER.items()):
            text = re.sub(rf"(>\s*)Unit {old}:", rf"\g<1>Unit ##{new}:", text)
            text = re.sub(rf"(>\s*)Bài {old}:", rf"\g<1>Bài ##{new}:", text)
        return text.replace("##", "")
    demo_theory = {}
    for nid in col.find_notes(f'"note:{VOCAB_MODEL}" -tag:EPV::*'):
        n = col.get_note(nid); before = list(n.fields); tags0 = list(n.tags)
        w0 = strip_html(n.fields[0]); u0 = int(n.fields[10]) if n.fields[10].isdigit() else 0
        if w0 in DEMO_WORD_FIX: n.fields[0] = DEMO_WORD_FIX[w0]
        if (w0, u0) in DEMO_ED1_ONLY and "EPV::demo_ban1" not in n.tags: n.tags.append("EPV::demo_ban1")
        m = re.match(r"\s*<i>\s*([^<]*?)\s*</i>\s*(.*)", n.fields[1], re.S)
        if m:
            pos = POS_FIX.get(m.group(1).strip().lower(), m.group(1).strip())
            n.fields[1] = f"<i>{pos}</i> {m.group(2).strip()}"
        if CFG.get("ipa_style", "uk") == "uk":
            n.fields[2] = uk_ipa(n.fields[2])
            if re.search(BATH, w0.lower()): n.fields[2] = re.sub(r"æ(?=ft|sk|sp|st|ntʃ|ns|mpl)", "ɑː", n.fields[2])   # BATH: æ (Mỹ) -> ɑː (Anh)
        if u0 in DEMO_EXTRA: n.fields[10] = f"B1-{u0:02d}"      # bài chỉ có ở bản 1: không trùng số với unit 9 bản 2
        if n.fields[10].isdigit() and int(n.fields[10]) in DEMO_RENUMBER: n.fields[10] = f"{DEMO_RENUMBER[int(n.fields[10])]:03d}"
        n.fields[12] = renum(n.fields[12])
        if u0 not in DEMO_EXTRA: demo_theory.setdefault(DEMO_RENUMBER.get(u0, u0), n.fields[12])
        if n.fields != before or n.tags != tags0: col.update_note(n); st["demo_notes_fixed"] += 1
    for nid in col.find_notes(f'"note:{THEORY_MODEL}" -tag:EPV::*'):
        n = col.get_note(nid); f0 = renum(n.fields[0])
        if "Contents" in strip_html(n.fields[0])[:40]: f0 = toc_field("adv")   # mục lục bản 2
        if f0 != n.fields[0]: n.fields[0] = f0; col.update_note(n); st["demo_notes_fixed"] += 1

    def deck(*parts): return col.decks.id("::".join(parts), create=True)
    top = {"adv": (ROOT, "Advanced"), "int": (ROOT, "Intermediate")}
    # 5. mục lục Intermediate
    if any(u["book"] == "int" for u in units):
        n = col.new_note(tm); n.guid = guid_for("int", 0, "__toc__")
        n.fields[0] = toc_field("int"); n.fields[3] = SOURCE; n.tags = ["EPV::int::toc"]
        col.add_note(n, deck(*top["int"], V_THEORY, "00-Contents"))
    # 6. note mới
    for u in sorted(units, key=lambda x: (x["book"], x["unit"])):
        b, un = u["book"], u["unit"]; sec, sub = section_of(b, un), unit_deck(b, un)
        tag = [f"EPV::{b}::u{un:02d}"]
        if u.get("supplement"):      # bổ sung thẻ cho unit demo: dùng lý thuyết của demo, không tạo note lý thuyết mới
            th = demo_theory.get(un, ""); tag.append("EPV::bosung_ban2")
        else:
            th = theory_field(b, un, u["theory_html"])
            n = col.new_note(tm); n.guid = guid_for(b, un, "__theory__")
            n.fields[0] = curly(th); n.fields[3] = SOURCE; n.tags = tag
            col.add_note(n, deck(*top[b], V_THEORY, sec, sub))
        d_look, d_listen = deck(*top[b], V_LOOK, sec, sub), deck(*top[b], V_LISTEN, sec, sub)
        for it in u["items"]:
            it["audio"] = "[sound:%s]" % col.media.add_file(os.path.join(KIT, "media", audio_name(b, un, it)))
            n = col.new_note(vm); n.guid = guid_for(b, un, it["word"].strip().lower(), it.get("sense", "").strip().lower())
            for i, v in enumerate(vocab_fields(u, it, th)): n.fields[i] = curly(v) if not v.startswith("[sound:") else v
            n.tags = tag; col.add_note(n, d_look)
            col.set_deck([c.id for c in n.cards() if c.ord == 1], d_listen)
            st["notes_added"] += 1
    col.decks.remove([nd.id for nd in col.decks.all_names_and_ids() if nd.name == "Default" and nd.id != 1])
    if os.path.exists(out): os.remove(out)
    col.export_anki_package(out_path=os.path.abspath(out), limit=ExportLimit(whole_collection=Empty()),
                            options=ExportAnkiPackageOptions(with_scheduling=False, with_deck_configs=True, with_media=True, legacy=False))
    col.close()
    print("BUILD OK ->", out, st)


if __name__ == "__main__":
    main()
