"""Biên dịch data/<book>_uNN.txt (định dạng gọn, xem README_VI.md) -> units/<book>_uNN.json.

Câu ví dụ: mặc định lấy NGUYÊN VĂN câu sách chứa headword (ưu tiên câu có headword in đậm ở trang lý thuyết,
sau đó trang bài tập), headword được bôi <b>. Ghi đè bằng trường ex=... (câu kit tự đặt → tag EVU::ex_kit).
Dùng: python3 tools/compile.py BOOK UNIT [UNIT ...]
"""
import sys, os, re, json
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POS = {"n": "noun", "v": "verb", "adj": "adjective", "adv": "adverb", "np": "noun phrase", "pn": "plural noun", "vp": "verb phrase",
       "pv": "phrasal verb", "idm": "idiom", "exp": "expression", "phr": "phrase", "prep": "preposition", "conj": "conjunction",
       "pron": "pronoun", "det": "determiner", "num": "number", "intj": "exclamation", "abbr": "abbreviation", "pref": "prefix",
       "suf": "suffix", "ap": "adjective phrase", "pp": "prepositional phrase", "mv": "modal verb", "un": "uncountable noun",
       "cn": "countable noun", "aux": "auxiliary verb", "dm": "discourse marker", "lw": "linking word", "sim": "simile", "prov": "proverb"}
INFL = r"(?:s|es|ed|d|ing|er|ers|est|ies|ied|ier|iest|'s|’s|n|en|ly)?"


def ital(s):
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", s.strip())


def rel(s):
    s = s.strip()
    if s in ("", "-"): return "<i>Not available</i>"
    out = []
    for part in s.split(";"):
        bits = [b.strip() for b in part.split(":", 2)]
        if len(bits) != 3 or not all(bits): raise ValueError(f"syn/ant sai dạng 'từ:loại:nghĩa' -> {part!r}")
        out.append(f"{bits[0]} <i>({bits[1]} {bits[2]})</i>")
    return ", ".join(out)


def grammar(word, pos, gloss, g):
    labels = {"G": "Grammar", "C": "Collocations / chunks", "W": "Word family", "M": "Common mistakes", "R": "Register", "N": "Note"}
    head = f"<i>{word[:1].upper() + word[1:]}</i> ({pos}) = {gloss}."
    parts = []
    for seg in g.split("//"):
        m = re.match(r"\s*([GCWMRN]):\s*(.*)", seg, re.S)
        if not m: raise ValueError(f"grammar: đoạn phải bắt đầu bằng G:/C:/W:/M:/R:/N: -> {seg!r}")
        parts.append(f"<b>{labels[m.group(1)]}</b>: {ital(m.group(2)).rstrip('.')}.")
    return " ".join([head] + parts)


def sentences(block):
    """Tách câu từ trang đã trích; nối dòng gãy của đoạn văn, tách dòng nhãn ngắn (tên trên tranh, tiêu đề)."""
    lines = [l.strip() for l in block.split("\n") if l.strip() and l.strip() not in ("Audio not supported",)]
    lines = [l for l in lines if not (re.fullmatch(r"\*\*[^*]*\*\*", l) and not re.search(r"[.?!]\**$", l) and len(l.split()) < 6)
             and not re.fullmatch(r"[\d\W]{1,4}", l)]
    lines = [re.sub(r"^\d{1,2}\s+(?=[A-Z‘“])", "", l) for l in lines]
    out, cur, last = [], "", ""
    for l in lines:
        plain = l.replace("**", "")
        if cur:
            pl = last.replace("**", "")
            if re.search(r"[.!?]$", pl): join = bool(re.match(r"^[a-z]", plain))
            else: join = len(pl) >= 55 or bool(re.match(r"^[a-z(‘“'\"]", plain)) or bool(re.search(r"[,;:–\-(/]$|\b(e\.g\.|i\.e\.)$", pl))
            if join: cur += " " + l; last = l; continue
            out.append(cur)
        cur = last = l
    if cur: out.append(cur)
    res = []
    for chunk in out:
        text = re.sub(r"\s+", " ", chunk).replace("** **", " ")
        text = re.sub(r"-\s+(?=[a-z])", "-", text)
        res += [x.strip() for x in re.split(r"(?<=[.!?…])\s+(?=[\"“‘(A-Z0-9*])", text) if x.strip()]
    return res


def word_rx(word):
    toks = re.findall(r"[A-Za-z0-9’'\-]+", re.sub(r"\(.*?\)|\bsth\b|\bsb\b|\bsomething\b|\bsomebody\b|\bsomeone\b|/.*", " ", word))
    if not toks: return None
    return re.compile(r"(?<![A-Za-z])" + r"(?:\*\*)?\s*".join(re.escape(t) + (INFL if i == len(toks) - 1 or len(toks) == 1 else INFL)
                                                         for i, t in enumerate(toks)) + r"(?![A-Za-z])", re.I)


def find_example(word, src):
    m = re.search(r"### LEFT\n(.*?)### RIGHT\n(.*?)### KEY", src, re.S)
    left, right = (m.group(1), m.group(2)) if m else (src, "")
    rx = word_rx(word)
    if not rx: return None
    cands = []
    for prio, block in ((0, left), (2, right)):
        for s in sentences(block):
            mm = rx.search(s.replace("**", ""))
            if not mm: continue
            bold = bool(re.search(r"\*\*[^*]*" + re.escape(mm.group(0).split()[0]) , s, re.I))
            n = len(s.split())
            bad = n > 45 or n < 4 or "……" in s or "…….." in s or ".........." in s
            cands.append((prio + (0 if bold else 1) + (5 if bad else 0), s))
    if not cands: return None
    cands.sort(key=lambda x: x[0])
    s = cands[0][1].replace("**", "")
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    return rx.sub(lambda x: f"<b>{x.group(0)}</b>", s, count=1)


def parse(path, src):
    lines = open(path, encoding="utf-8").read().split("\n")
    u = {"title_vi": "", "theory": [], "items": [], "errors": []}
    mode = None
    for ln, raw in enumerate(lines, 1):
        l = raw.rstrip()
        if not l.strip() or l.lstrip().startswith("#!"): continue
        if l.startswith("@title_vi:"): u["title_vi"] = l.split(":", 1)[1].strip(); continue
        if l.strip() == "@theory": mode = "t"; continue
        if l.strip() == "@items": mode = "i"; continue
        if mode == "t":
            u["theory"].append(l); continue
        if mode == "i":
            f = [x.strip() for x in l.split(" | ")]
            opt = {}
            while f and re.match(r"^(ex|sense|exvi)=", f[-1]):
                k, v = f.pop().split("=", 1); opt[k] = v.strip()
            if len(f) != 10:
                u["errors"].append(f"dòng {ln}: cần 10 trường (+ ex=/sense=), có {len(f)}: {l[:80]}"); continue
            w, pos, ipa, den, dvi, gl, exvi, syn, ant, g = f
            pos = POS.get(pos, pos)
            try:
                it = {"word": w, "sense": opt.get("sense", ""), "pos": pos, "ipa": ipa, "def_en": den, "def_vi": dvi, "gloss_vi": gl,
                      "synonyms": rel(syn), "antonyms": rel(ant), "grammar_vi": grammar(w, pos, gl, g)}
            except ValueError as e:
                u["errors"].append(f"dòng {ln} '{w}': {e}"); continue
            if "ex" in opt:
                en = ital(opt["ex"]).replace("[", "<b>").replace("]", "</b>"); it["ex_kit"] = True
            else:
                en = find_example(w, src)
                if not en: u["errors"].append(f"dòng {ln} '{w}': không thấy câu sách chứa từ – thêm ex=... ([từ] để bôi đậm)"); continue
            it["example"] = {"en": en, "vi": exvi.replace("[", "<b>").replace("]", "</b>")}
            u["items"].append(it)
    return u


def bold(s):
    return re.sub(r"\*(.+?)\*", r"<b>\1</b>", s.strip())


def theory_html(lines):
    """## A | Heading EN | Heading VI  ;  EN ‖ VI  (đoạn) ;  - term ‖ nghĩa (danh sách)."""
    out, ul = [], []
    def flush():
        if ul: out.append("<ul>" + "".join(f"<li>{x}</li>" for x in ul) + "</ul>"); ul.clear()
    for l in lines:
        if l.startswith("## "):
            flush(); p = [x.strip() for x in l[3:].split("|")]
            out.append(f"<p><b>{p[0]}. {bold(p[1])}</b><br><i>{p[0]}. {bold(p[2])}</i></p>")
        elif l.lstrip().startswith("- "):
            en, _, vi = l.lstrip()[2:].partition("‖"); ul.append(f"{bold(en)}" + (f" – <i>{bold(vi)}</i>" if vi.strip() else ""))
        else:
            flush(); en, _, vi = l.partition("‖")
            out.append(f"<p>{bold(en)}</p>" + (f"<p><i>{bold(vi)}</i></p>" if vi.strip() else ""))
    flush()
    return " ".join(out)


def main():
    book = sys.argv[1]; bad = 0
    for un in map(int, sys.argv[2:]):
        name = f"{book}_u{un:02d}"
        src = open(os.path.join(KIT, "src", name + ".txt"), encoding="utf-8").read()
        u = parse(os.path.join(KIT, "data", name + ".txt"), src)
        for e in u["errors"]: print(f"  LỖI {name}: {e}")
        bad += len(u["errors"])
        out = {"book": book, "unit": un, "title_vi": u["title_vi"], "theory_html": theory_html(u["theory"]), "items": u["items"]}
        json.dump(out, open(os.path.join(KIT, "units", name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{name}: {len(u['items'])} mục, {sum(1 for i in u['items'] if i.get('ex_kit'))} câu kit đặt, {len(u['errors'])} lỗi")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
