#!/usr/bin/env python3
"""Build 1 deck Grammar in Use từ units/<book>_uNNN.json, schema theo deck mẫu
base/English Grammar In Use (Intermediate).apkg.

Dùng:  python3 tools/build_deck.py BOOK [--check-only]   → out/<Root>.apkg
 - Note type & giao diện lấy nguyên từ deck mẫu: "Tóm tắt++" (lý thuyết) + "MCQ custom shuffled (Grammar)".
   Note mẫu (sách Intermediate) bị xoá, chỉ giữ note type.
 - Deck: <Root>::A. Lý thuyết::NN-Section::NNN Title  và  <Root>::B. Câu hỏi::NN-Section::NNN Title
   (+ A. Lý thuyết::NN-Appendix nếu có data/<book>_aNN.txt).
 - GUID cố định: egu|book|unit|__theory__ và egu|book|unit|câu hỏi|đáp án -> import lại chỉ cập nhật.
"""
import sys, os, re, json, hashlib, tempfile, html, glob
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
BOOKS = json.load(open(os.path.join(HERE, "books.json"), encoding="utf-8"))
BASE = os.path.join(KIT, "base", "English Grammar In Use (Intermediate).apkg")
THEORY_MODEL, MCQ_MODEL = "Tóm tắt++", "MCQ custom shuffled (Grammar)"
SOURCE = ""          # người dùng yêu cầu bỏ chữ "Anki Support Vietnam" khỏi mọi deck
A, B = "A. Lý thuyết", "B. Câu hỏi"


def strip_html(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def curly(s): return "".join(p if p.startswith("<") else p.replace("'", "’") for p in re.split(r"(<[^>]+>)", s))


def guid_for(*parts):
    h = hashlib.sha1("|".join(map(str, ("egu",) + parts)).encode("utf-8")).digest()
    a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./:;<=>?@[]^_`{|}~"
    n = int.from_bytes(h[:8], "big"); out = ""
    while n: n, r = divmod(n, len(a)); out += a[r]
    return "egu" + out


def sections(book):
    return {s: f"{i:02d}-{s}" for i, s in enumerate(BOOKS[book]["sections"], 1)}


def unit_deck(book, un):
    return f"{un:03d} " + BOOKS[book]["units"][str(un)]["title"].replace("::", ":")


def tag_balance_errors(s):
    errs = []
    for t in ("b", "i", "p", "table", "thead", "tbody", "tr", "td", "th", "ul", "li", "font"):
        o = len(re.findall(rf"<{t}(\s[^>]*)?>", s)); c = len(re.findall(rf"</{t}>", s))
        if o != c: errs.append(f"thẻ <{t}> mở {o} / đóng {c}")
    return errs


def theory_field(book, u, egu=None):
    un = u["unit"]; info = BOOKS[book]["units"][str(un)]; t = html.escape(info["title"], quote=False)
    lab, lab_vi = info.get("label", f"Unit {un}"), info.get("label_vi", f"Bài {un}")
    t = t.replace(f" ({lab})", "")
    out = (f'<p style="text-align: center;"><b><font color="#006ba6">{lab} – {t}</font></b></p>\n'
           f'<p style="text-align: center;"><i>{lab_vi} – {html.escape(u["title_vi"], quote=False)}</i></p>\n'
           f'<hr style="text-align: center;">\n\n' + u["theory_html"])
    for e in u.get("egu_units", []):      # sup: lý thuyết các unit EGU liên quan, lấy nguyên từ deck mẫu
        out += '\n\n<hr style="text-align: center;">\n\n' + egu[e]
    return out


def egu_theory(col):
    """{số unit: nội dung lý thuyết} từ note "Tóm tắt++" của deck mẫu Intermediate (đọc trước khi xoá note mẫu)."""
    m = {}
    for nid in col.find_notes(f'note:"{THEORY_MODEL}"'):
        n = col.get_note(nid); last = col.decks.name(col.get_card(n.card_ids()[0]).did).split("::")[-1]
        g = re.match(r"(\d+) ", last)
        if g: m[int(g.group(1))] = n["Câu hỏi"]
    return m


def validate(u, fname, book):
    E = []
    if u.get("book") != book or str(u.get("unit")) not in BOOKS[book]["units"]: E.append("book/unit sai")
    if not u.get("title_vi"): E.append("thiếu title_vi")
    body = u.get("theory_html", "")
    if len(strip_html(body)) < 300: E.append("theory_html quá ngắn")
    E += ["theory_html: " + e for e in tag_balance_errors(body)]
    if len(u.get("mcq", [])) < 15: E.append(f"quá ít MCQ ({len(u.get('mcq', []))})")
    for k, q in enumerate(u.get("mcq", []), 1):
        p = f"MCQ#{k} '{strip_html(q['question'])[:50]}'"
        for f in ("question", "a", "b", "c", "full", "vi", "expl"):
            if not strip_html(q.get(f, "")): E.append(f"{p}: thiếu {f}")
            E += [f"{p}: {f} " + e for e in tag_balance_errors(q.get(f, ""))]
        if "<b>" not in q["full"] and q["a"] not in ("–", "-", "—"): E.append(f"{p}: câu hoàn chỉnh thiếu <b>")
        if "<b>" not in q["vi"]: E.append(f"{p}: bản dịch thiếu <b>")
    return [f"{fname}: {e}" for e in E]


def appendix_field(a):
    return (f'<p style="text-align: center;"><b><font color="#006ba6">{html.escape(a["title_en"], quote=False)}</font></b></p>\n'
            f'<p style="text-align: center;"><i>{html.escape(a["title_vi"], quote=False)}</i></p>\n'
            f'<hr style="text-align: center;">\n\n' + a["theory_html"])


def main():
    book = sys.argv[1]; root = BOOKS[book]["root"]
    units, errs = [], []
    for fn in sorted(glob.glob(os.path.join(KIT, "units", f"{book}_u*.json"))):
        u = json.load(open(fn, encoding="utf-8")); errs += validate(u, os.path.basename(fn), book); units.append(u)
    apps = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(KIT, "units", f"{book}_a*.json")))]
    if errs: print("LỖI VALIDATE:\n  " + "\n  ".join(errs)); sys.exit(2)
    print(f"OK validate {book}: {len(units)} unit, {sum(len(u['mcq']) for u in units)} MCQ, {len(apps)} phụ lục")
    if "--check-only" in sys.argv: return
    from anki.collection import Collection, ImportAnkiPackageRequest, ImportAnkiPackageOptions, ExportAnkiPackageOptions
    from anki.import_export_pb2 import ExportLimit
    from anki.generic_pb2 import Empty
    d = tempfile.mkdtemp(); col = Collection(os.path.join(d, "c.anki2"))
    col.import_anki_package(ImportAnkiPackageRequest(package_path=BASE,
                                                     options=ImportAnkiPackageOptions(with_scheduling=False, with_deck_configs=True)))
    tm, mm = col.models.by_name(THEORY_MODEL), col.models.by_name(MCQ_MODEL)
    egu = egu_theory(col)
    miss = sorted({e for u in units for e in u.get("egu_units", [])} - set(egu))
    if miss: print("LỖI: deck mẫu không có lý thuyết unit", miss); sys.exit(2)
    col.remove_notes(list(col.find_notes("")))
    col.decks.remove([nd.id for nd in col.decks.all_names_and_ids() if nd.name.startswith("English Grammar In Use")])
    for m in col.models.all():          # chỉ giữ 2 note type của deck mẫu
        if m["name"] not in (THEORY_MODEL, MCQ_MODEL) and not col.models.use_count(m): col.models.remove(m["id"])

    def deck(*parts): return col.decks.id("::".join(parts), create=True)
    sec = sections(book); st = {"theory": 0, "mcq": 0, "appendix": 0}
    for u in sorted(units, key=lambda x: x["unit"]):
        un = u["unit"]; s = sec[BOOKS[book]["units"][str(un)]["section"]]; sub = unit_deck(book, un)
        tag = [f"EGU::{book}::u{un:03d}"]; th = curly(theory_field(book, u, egu))
        n = col.new_note(tm); n.guid = guid_for(book, un, "__theory__")
        n["Câu hỏi"] = th; n["Nguồn"] = SOURCE; n.tags = tag
        col.add_note(n, deck(root, A, s, sub)); st["theory"] += 1
        dq = deck(root, B, s, sub)
        for q in u["mcq"]:
            n = col.new_note(mm); n.guid = guid_for(book, un, q["key"])
            for f, k in (("Question", "question"), ("a", "a"), ("b", "b"), ("c", "c"), ("Câu hoàn chỉnh", "full"),
                         ("Dịch ví dụ", "vi"), ("Giải thích", "expl")): n[f] = curly(q[k])
            n["Answer"] = "100"; n["Đề mục"] = "Chọn đáp án đúng nhất"; n["Nguồn"] = SOURCE; n["Bài giảng lý thuyết"] = th
            n.tags = tag; col.add_note(n, dq); st["mcq"] += 1
    if apps:
        app_sec = f"{len(sec) + 1:02d}-Appendix"
        for a in sorted(apps, key=lambda x: x["n"]):
            n = col.new_note(tm); n.guid = guid_for(book, "appendix", a["n"])
            n["Câu hỏi"] = curly(appendix_field(a)); n["Nguồn"] = SOURCE; n.tags = [f"EGU::{book}::appendix"]
            col.add_note(n, deck(root, A, app_sec, a["title_en"].replace("::", ":"))); st["appendix"] += 1
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
