#!/usr/bin/env python3
"""Build 1 deck English Vocabulary in Use cho 1 sách từ units/<book>_uNN.json (+ deck demo nếu có).

Dùng:  python3 tools/build_deck.py BOOK [--check-only]   → out/<Root>.apkg
 - Note type & giao diện lấy từ deck demo (base/English Vocabulary In Use (Upper-Intermediate).apkg):
   "(Vocab In Use) Nhìn từ đoán nghĩa" (13 field, 2 thẻ) + "Tóm tắt".
 - Sách có demo (upp): giữ nguyên note demo (GUID, audio Azure), chỉ đổi IPA Mỹ -> Anh (config.ipa_style),
   bỏ qua unit đã có trong demo. Sách khác: bỏ note demo, chỉ giữ note type.
 - GUID cố định: evu|book|unit|word|sense -> import lại chỉ cập nhật, không nhân đôi.
 - Deck: <Root>::{Lý thuyết, Từ vựng (nhìn từ, đoán nghĩa), Từ vựng (nghe, gõ từ đúng)}::NN-Section::NN-Unit
   (thẻ 1 -> nhìn từ, thẻ 2 -> nghe), như demo. 01-Contents = mục lục song ngữ.
"""
import sys, os, re, json, hashlib, tempfile, html, glob
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from make_audio import audio_name
BOOKS = json.load(open(os.path.join(HERE, "books.json"), encoding="utf-8"))
CFG = json.load(open(os.path.join(KIT, "config.json"), encoding="utf-8"))
MODEL_BASE = os.path.join(KIT, "base", "English Vocabulary In Use (Upper-Intermediate).apkg")
DEMO = {"upp": MODEL_BASE}
VOCAB_MODEL, THEORY_MODEL = "(Vocab In Use) Nhìn từ đoán nghĩa", "Tóm tắt"
SOURCE = ""          # người dùng yêu cầu bỏ chữ "Anki Support Vietnam" khỏi mọi deck
V_THEORY, V_LOOK, V_LISTEN = "Lý thuyết", "Từ vựng (nhìn từ, đoán nghĩa)", "Từ vựng (nghe, gõ từ đúng)"
HR = '<hr style="border: none; height: 0.5px; background-color: #e0e0e0;">'


def strip_html(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def curly(s): return "".join(p if p.startswith("<") else p.replace("'", "’") for p in re.split(r"(<[^>]+>)", s))


def guid_for(*parts):
    h = hashlib.sha1("|".join(map(str, parts)).encode("utf-8")).digest()
    a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./:;<=>?@[]^_`{|}~"
    n = int.from_bytes(h[:8], "big"); out = ""
    while n: n, r = divmod(n, len(a)); out += a[r]
    return "evu" + out


def section_of(book, unit):
    for i, (a, b, en, vi) in enumerate(BOOKS[book]["sections"], 2):
        if a <= unit <= b: return f"{i:02d}-{en}"
    raise ValueError(f"unit {unit} ngoài phạm vi sách {book}")


def unit_deck(book, unit): return f"{unit:02d}-{BOOKS[book]['units'][str(unit)]['en']}"


def tag_balance_errors(s):
    errs = []
    for t in ("b", "i", "p", "div", "table", "tr", "td", "th", "ul", "li", "span"):
        o = len(re.findall(rf"<{t}(\s[^>]*)?>", s)); c = len(re.findall(rf"</{t}>", s))
        if o != c: errs.append(f"thẻ <{t}> mở {o} / đóng {c}")
    return errs


V = "aeiouæʌɑɒɔəɜɪʊɛː"
def uk_ipa(ipa):
    s = ipa.replace("oʊ", "əʊ").replace("ɛ", "e").replace("ɝ", "ɜː").replace("ɚ", "ə").replace("ɹ", "r")
    s = re.sub(r"ɑ(?!ː)r?", lambda m: "ɑː" if m.group(0) == "ɑr" else "ɒ", s)
    s = re.sub(r"ɔ(?![ːɪ])(?=[fsŋgθ])", "ɒ", s)
    s = re.sub(r"ɔ(?![ːɪ])", "ɔː", s)
    out = []
    for w in s.split(" "):
        w = re.sub(rf"(?<=[{V}])r(?=[^{V}ˈˌ/]|/|$)", "", w)
        w = re.sub(rf"(?<=[{V}])r(?=[ˈˌ][^{V}])", "", w)
        out.append(w)
    return " ".join(out)


def validate(u, fname, book):
    E = []
    if u.get("book") != book or str(u.get("unit")) not in BOOKS[book]["units"]: E.append("book/unit sai")
    if not u.get("title_vi"): E.append("thiếu title_vi")
    body = u.get("theory_html", "")
    if len(strip_html(body)) < 150: E.append("theory_html quá ngắn")
    E += ["theory_html: " + e for e in tag_balance_errors(body)]
    E += [f"thiếu ảnh img/{f} – chạy tools/mkimg.py" for f in re.findall(r'<img src="([^"]+)"', body) if not os.path.exists(os.path.join(KIT, "img", f))]
    if len(u.get("items", [])) < 3: E.append("quá ít mục")
    seen = set()
    for k, it in enumerate(u.get("items", []), 1):
        w = it.get("word", "").strip(); p = f"#{k} '{w}'"
        key = (w.lower(), it.get("sense", "").lower())
        if key in seen: E.append(f"{p}: trùng word+sense trong unit")
        seen.add(key)
        for f in ("pos", "def_en", "ipa", "def_vi", "gloss_vi", "grammar_vi", "synonyms", "antonyms"):
            if not str(it.get(f, "")).strip(): E.append(f"{p}: thiếu {f}")
        if not re.fullmatch(r"/[^/]+/", it.get("ipa", "")): E.append(f"{p}: ipa phải dạng /.../")
        for x in ("en", "vi"):
            if "<b>" not in it.get("example", {}).get(x, ""): E.append(f"{p}: example.{x} thiếu <b>")
        if not it.get("def_en", "").rstrip().endswith((".", "?", "!", "…")): E.append(f"{p}: def_en phải kết thúc bằng dấu chấm")
        if not it.get("def_vi", "").rstrip().endswith((".", "?", "!", "…")): E.append(f"{p}: def_vi phải kết thúc bằng dấu chấm")
        if not os.path.exists(os.path.join(KIT, "media", audio_name(book, u["unit"], it))): E.append(f"{p}: thiếu audio – chạy evu.py audio")
        for f in ("grammar_vi", "synonyms", "antonyms"): E += [f"{p}: {f} " + e for e in tag_balance_errors(it.get(f, ""))]
    return [f"{fname}: {e}" for e in E]


def theory_field(book, u):
    t = BOOKS[book]["units"][str(u["unit"])]["en"]
    head = (f'<div style="text-align: center;"><span style="color: rgb(0, 107, 166);"><b>Unit {u["unit"]}: {t}</b></span>'
            f'<div><i>Bài {u["unit"]}: {u["title_vi"]}</i></div></div> {HR} ')
    return head + u["theory_html"].replace("<hr>", HR)


def toc_field(book, units):
    b = BOOKS[book]; vi = {u["unit"]: u["title_vi"] for u in units}
    parts = [f'<p style="text-align: center;"><font color="#006ba6"><b>Unit 0: Contents</b></font><br><i>Mục lục</i></p> {HR}']
    for a, z, en, svi in b["sections"]:
        parts.append(f"<p><b>{en}</b><br><i>{svi}</i></p>" + "".join(
            f"<p><b>{n}&nbsp;{b['units'][str(n)]['en']}</b><br><i>{n}&nbsp;{vi.get(n, '')}</i></p>" for n in range(a, z + 1)) + " " + HR)
    return " ".join(parts)


def vocab_fields(u, it):
    return [it["word"].strip(), f'<i>{it["pos"]}</i> {it["def_en"].strip()}', it["ipa"].strip(), it["def_vi"].strip(), it["gloss_vi"].strip(),
            it["example"]["en"].strip(), it["example"]["vi"].strip(), it["antonyms"], it["synonyms"], it["grammar_vi"].strip(),
            it.get("audio", ""), f'{u["unit"]:03d}', SOURCE]


def demo_units(book):
    return set(BOOKS[book].get("demo_units", []))


def main():
    book = sys.argv[1]; root = BOOKS[book]["root"]
    units, errs = [], []
    for fn in sorted(glob.glob(os.path.join(KIT, "units", f"{book}_u*.json"))):
        u = json.load(open(fn, encoding="utf-8")); errs += validate(u, os.path.basename(fn), book); units.append(u)
    if errs: print("LỖI VALIDATE:\n  " + "\n  ".join(errs)); sys.exit(2)
    print(f"OK validate {book}: {len(units)} unit, {sum(len(u['items']) for u in units)} mục")
    if "--check-only" in sys.argv: return
    from anki.collection import Collection, ImportAnkiPackageRequest, ImportAnkiPackageOptions, ExportAnkiPackageOptions
    from anki.import_export_pb2 import ExportLimit
    from anki.generic_pb2 import Empty
    d = tempfile.mkdtemp(); col = Collection(os.path.join(d, "c.anki2"))
    col.import_anki_package(ImportAnkiPackageRequest(package_path=DEMO.get(book, MODEL_BASE),
                                                     options=ImportAnkiPackageOptions(with_scheduling=False, with_deck_configs=True)))
    vm, tm = col.models.by_name(VOCAB_MODEL), col.models.by_name(THEORY_MODEL)
    st = {"demo_notes_kept": 0, "demo_ipa_uk": 0, "notes_added": 0, "theory_added": 0}
    if book in DEMO:
        for nid in col.find_notes(f'"note:{VOCAB_MODEL}"'):
            n = col.get_note(nid); st["demo_notes_kept"] += 1
            if CFG.get("ipa_style") == "uk":
                new = uk_ipa(n.fields[2])
                if new != n.fields[2]: n.fields[2] = new; col.update_note(n); st["demo_ipa_uk"] += 1
        st["demo_notes_kept"] += len(col.find_notes(f'"note:{THEORY_MODEL}"'))
    else:
        col.remove_notes(list(col.find_notes("")))
        col.decks.remove([nd.id for nd in col.decks.all_names_and_ids() if nd.name.startswith("English Vocabulary In Use") ])

    def deck(*parts): return col.decks.id("::".join(parts), create=True)
    toc_deck = deck(root, V_THEORY, "01-Contents")
    olds = [nid for nid in col.find_notes(f'"note:{THEORY_MODEL}" "deck:{root}::{V_THEORY}::01-Contents"')]
    if olds:      # demo: thay nội dung mục lục, giữ GUID
        n = col.get_note(olds[0]); n.fields[0] = toc_field(book, units); col.update_note(n)
    else:
        n = col.new_note(tm); n.guid = guid_for(book, 0, "__toc__"); n.fields[0] = toc_field(book, units); n.fields[3] = SOURCE
        n.tags = [f"EVU::{book}::toc"]; col.add_note(n, toc_deck)
    for u in sorted(units, key=lambda x: x["unit"]):
        un = u["unit"]
        if un in demo_units(book): continue
        sec, sub = section_of(book, un), unit_deck(book, un); tag = [f"EVU::{book}::u{un:02d}"]
        n = col.new_note(tm); n.guid = guid_for(book, un, "__theory__")
        for f in re.findall(r'<img src="([^"]+)"', u["theory_html"]): col.media.add_file(os.path.join(KIT, "img", f))
        n.fields[0] = curly(theory_field(book, u)); n.fields[3] = SOURCE; n.tags = tag
        col.add_note(n, deck(root, V_THEORY, sec, sub)); st["theory_added"] += 1
        d_look, d_listen = deck(root, V_LOOK, sec, sub), deck(root, V_LISTEN, sec, sub)
        for it in u["items"]:
            it["audio"] = "[sound:%s]" % col.media.add_file(os.path.join(KIT, "media", audio_name(book, un, it)))
            n = col.new_note(vm); n.guid = guid_for(book, un, it["word"].strip().lower(), it.get("sense", "").strip().lower())
            for i, v in enumerate(vocab_fields(u, it)): n.fields[i] = v if v.startswith("[sound:") else curly(v)
            n.tags = tag + (["EVU::ex_kit"] if it.get("ex_kit") else []); col.add_note(n, d_look)
            col.set_deck([c.id for c in n.cards() if c.ord == 1], d_listen); st["notes_added"] += 1
    col.decks.remove([nd.id for nd in col.decks.all_names_and_ids() if nd.name == "Default" and nd.id != 1])
    out = os.path.join(KIT, "out", root + ".apkg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out): os.remove(out)
    from nobrand import strip_brand
    print("Bỏ chữ Anki Support Vietnam:", strip_brand(col))
    col.export_anki_package(out_path=out, limit=ExportLimit(whole_collection=Empty()),
                            options=ExportAnkiPackageOptions(with_scheduling=False, with_deck_configs=True, with_media=True, legacy=False))
    col.close()
    print("BUILD OK ->", out, st)


if __name__ == "__main__":
    main()
