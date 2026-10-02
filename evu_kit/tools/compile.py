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
       "cn": "countable noun", "aux": "auxiliary verb", "dm": "discourse marker", "lw": "linking word", "sim": "simile", "prov": "proverb",
       "cl": "fixed expression", "excl": "exclamation", "adjp": "adjective phrase", "st": "structure"}
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
    lines = ["@@BREAK@@" if l in ("•", "■", "–", "-", "▪", "●") else l for l in lines]
    lines = [l for l in lines if not (re.fullmatch(r"\*\*[^*]*\*\*", l) and not re.search(r"[.?!]\**$", l) and len(l.split()) < 6
                                      and not re.match(r"^\*\*[a-z]", l))
             and not re.fullmatch(r"[\d\W]{1,4}", l)]
    lines = [re.sub(r"^\d{1,2}\s+(?=[A-Z‘“])", "", l) for l in lines]
    isl = lambda x: bool(re.fullmatch(r"\*\*[^*]+\*\*", x)) and len(x.split()) < 5 and not re.search(r"[.!?]\**$", x)
    lines = [l for i, l in enumerate(lines) if not (isl(l) and 0 < i < len(lines) - 1 and not re.search(r"[.!?:,;–\-]\**$", lines[i - 1])
                                                    and re.match(r"^[a-z]", lines[i + 1].replace("**", "")))]
    out, cur, last = [], "", ""
    lab = lambda x: bool(re.fullmatch(r"\*\*[^*]+\*\*", x)) and len(x.split()) < 5 and not re.search(r"[.!?]\**$", x)
    for l in lines:
        if l == "@@BREAK@@":
            if cur: out.append(cur)
            cur = last = ""; continue
        plain = l.replace("**", "")
        if cur:
            pl = last.replace("**", "")
            if lab(l): join = bool(re.search(r"[,;:–\-(/]$", pl))
            elif lab(last): join = bool(re.match(r"^(and|or|but)\b|^[,.;:]", plain))
            elif re.search(r"[.!?)\]]$", pl): join = bool(re.match(r"^[a-z]", plain))
            else: join = len(pl) >= 40 or bool(re.match(r"^[a-z0-9(‘“'\"]", plain)) or bool(re.search(r"[,;:–\-(/]$|\b(e\.g\.|i\.e\.)$", pl))
            if join: cur += " " + l; last = l; continue
            out.append(cur)
        cur = last = l
    if cur: out.append(cur)
    res = []
    for chunk in out:
        text = re.sub(r"\s+", " ", chunk).replace("** **", " ")
        text = re.sub(r"\s*/[^/\s]*[ˈˌːəɪʊʌæɒɔθðʃʒŋ'I][^/\s]*\s?/", "", text)      # bỏ phiên âm /…/ chen trong câu
        text = re.sub(r"\s*([.!?…,;:])\*\*", r"**\1", text)
        text = re.sub(r"(?<=[a-z])-\s+(?=[a-z])", "-", text)
        res += [x.strip() for x in re.split(r"(?<=[.!?…])\s+(?=[\"“‘(A-Z0-9*])", text) if x.strip()]
    return res


IRR_SRC = """be is are was were been being am|have has had having|do does did done doing|go goes went gone going|get gets got gotten getting|make makes made making|take takes took taken taking|come comes came coming|give gives gave given giving|bring brings brought bringing|buy bought|catch caught|choose chose chosen|drink drank drunk|drive drove driven|eat ate eaten|fall fell fallen|feel felt|find found|fly flew flown|forget forgot forgotten|grow grew grown|hear heard|hold held|keep kept|know knew known|leave left|lend lent|lose lost|meet met|pay paid|put|read|ride rode ridden|ring rang rung|run ran|say said|see saw seen|sell sold|send sent|shake shook shaken|sing sang sung|sit sat|sleep slept|speak spoke spoken|spend spent|stand stood|steal stole stolen|swim swam swum|teach taught|tell told|think thought|throw threw thrown|understand understood|wake woke woken|wear wore worn|win won|write wrote written|break broke broken|begin began begun|build built|cut|fight fought|hide hid hidden|hit|hurt|let|lie lay lain|light lit|mean meant|set|shut|show showed shown|sink sank sunk|feed fed|freeze froze frozen|lead led|bite bit bitten|blow blew blown|draw drew drawn|dig dug|hang hung|shoot shot|spill spilt spilled|spread|stick stuck|strike struck|swear swore sworn|tear tore torn|beat beaten|bend bent|bet|burn burnt burned|dream dreamt dreamed|learn learnt learned|smell smelt smelled|spell spelt spelled"""
IRR = {}
for grp in IRR_SRC.split("|"):
    fs = grp.split()
    for f in fs: IRR.setdefault(f, set()).update(fs)


def tok_rx(t, last):
    forms = sorted(IRR.get(t.lower(), {t.lower()}), key=len, reverse=True)
    alt = "|".join(re.escape(f) for f in forms)
    extra = ""
    w = t.lower()
    if len(w) > 2 and w.endswith("e"): extra += "|" + re.escape(w[:-1]) + "(?:ing|ed|er|ers|est)"
    if len(w) > 2 and w.endswith("y"): extra += "|" + re.escape(w[:-1]) + "(?:ies|ied|ier|iest)"
    if len(w) > 2 and re.search(r"[^aeiou][aeiou][bdgklmnprt]$", w): extra += "|" + re.escape(w + w[-1]) + "(?:ing|ed|er|ers)"
    return f"(?:(?:{alt}){INFL}{extra})(?![A-Za-z])"


def word_rx(word):
    toks = re.findall(r"[A-Za-z0-9’'\-]+", re.sub(r"\(.*?\)|\bsth\b|\bsb\b|\bsomething\b|\bsomebody\b|\bsomeone\b|/.*", " ", word))
    if not toks: return None
    parts = [tok_rx(t, i == len(toks) - 1) for i, t in enumerate(toks)]
    PART = {"on", "off", "up", "down", "in", "out", "away", "back", "over", "round", "around", "through", "along"}
    sep = [r"(?:\*\*)?\s*(?:\*\*)?"] * (len(toks) - 1)
    if len(toks) >= 2 and toks[-1].lower() in PART:      # phrasal verb tách được: cho phép ≤3 từ chen giữa
        sep[-1] = r"(?:\*\*)?\s*(?:\*\*)?(?:[A-Za-z’'\-]+\s+){0,3}?(?:\*\*)?"
    CON = {"have": "ve", "will": "ll", "are": "re", "is": "s", "am": "m", "would": "d", "had": "d", "be": "(?:m|re|s)"}
    first = r"(?<![A-Za-z])" + parts[0]
    if toks[0].lower() in CON: first = f"(?:{first}|(?<=[A-Za-z])[’']{CON[toks[0].lower()]})"
    rx = first
    for sp, pt in zip(sep, parts[1:]): rx += sp + pt
    return re.compile(rx + r"(?![A-Za-z])", re.I)


def find_example(word, src):
    m = re.search(r"### LEFT\n(.*?)### RIGHT\n(.*?)### KEY", src, re.S)
    left, right = (m.group(1), m.group(2)) if m else (src, "")
    rx = word_rx(word)
    if not rx: return None
    cands = []
    for prio, block in ((0, left), (2, right)):
        for s in sentences(block):
            mm = rx.search(re.sub(r"\s*\[[^\]]*\]|\s*\((?:See|see) [^)]*\)", "", s.replace("**", "")))
            if not mm: continue
            bold = bool(re.search(r"\*\*[^*]*" + re.escape(mm.group(0).split()[0]) , s, re.I))
            s2 = re.sub(r"\s*\[[^\]]*\]", "", s).strip()
            n = len(s2.split())
            nb = len(" ".join(re.findall(r"\*\*([^*]+)\*\*", s2)).split())
            bad = n > 45 or n < 2 or (re.fullmatch(r"\*\*[^*]+\*\*", s2) is not None) or (nb / n > 0.6 and n >= 4 and not re.search(r"[.!?]\**$", s2)) or "……" in s or "…….." in s or ".........." in s
            if not bad: cands.append((prio + (0 if bold else 1), s))
    if not cands: return None
    cands.sort(key=lambda x: x[0])
    s = cands[0][1].replace("**", "")
    s = re.sub(r"\s*\[[^\]]*\]", "", s)                       # bỏ chú giải [..] của sách khỏi câu ví dụ
    s = re.sub(r"\s*\((?:See|see) [^)]*\)", "", s).strip()
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    return rx.sub(lambda x: f"<b>{x.group(0)}</b>", s, count=1)


LABEL = re.compile(r"^(?:[AB]:\s+|[AB]\s+(?=(?:<b>)?(?:Do|Did|Are|And|Have|Is|What|Where|When|The|Can|If|Yes|No|She|He|We|I|It|They|You|Oh|Excuse|How|Go|Take|Turn|Usually)\b))")


LISTLBL = re.compile(r"^[b-h]\s+(?=<b>)")   # nhãn liệt kê b/c/d… của sách ('a' trùng mạo từ → sửa tay)
def drop_label(en):
    """Bỏ nhãn người nói A:/B: ở câu một lượt (giữ nguyên hội thoại hai lượt A: … B: …)."""
    if len(re.findall(r"(?:^|\s)[AB]:\s", en)) >= 2: return en
    en = LABEL.sub("", en, count=1)
    en = LISTLBL.sub("", en, count=1)
    return ROLE.sub("", en, count=1)


ROLE = re.compile(r"^(?:Customer|Waiter|Shop assistant|Receptionist|Guest|[A-Z]{3,}(?=\s+I\b))\s+(?=(?:<b>)?[A-Z‘“'(])")


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
            for x in [x for x in f if re.match(r"^(ex|exb|sense)=", x)]:
                k, v = x.split("=", 1); opt[k] = v.strip(); f.remove(x)
            if len(f) != 10:
                u["errors"].append(f"dòng {ln}: cần 10 trường (+ ex=/sense=), có {len(f)}: {l[:80]}"); continue
            w, pos, ipa, den, dvi, gl, exvi, syn, ant, g = f
            pos = POS.get(pos, pos)
            try:
                it = {"word": w, "sense": opt.get("sense", ""), "pos": pos, "ipa": ipa, "def_en": den, "def_vi": dvi, "gloss_vi": gl,
                      "synonyms": rel(syn), "antonyms": rel(ant), "grammar_vi": grammar(w, pos, gl, g)}
            except ValueError as e:
                u["errors"].append(f"dòng {ln} '{w}': {e}"); continue
            if "exb" in opt:      # câu sách ghép lại thủ công (bảng/hai cột bị trích rời) – vẫn là câu của sách
                en = ital(opt["exb"]).replace("[", "<b>").replace("]", "</b>")
            elif "ex" in opt:
                en = ital(opt["ex"]).replace("[", "<b>").replace("]", "</b>"); it["ex_kit"] = True
            else:
                en = find_example(w, src)
                if not en: u["errors"].append(f"dòng {ln} '{w}': không thấy câu sách chứa từ – thêm ex=... ([từ] để bôi đậm)"); continue
            it["example"] = {"en": drop_label(en), "vi": exvi.replace("[", "<b>").replace("]", "</b>")}
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
    for un in [int(x) for x in sys.argv[2:] if x != '-q']:
        name = f"{book}_u{un:02d}"
        src = open(os.path.join(KIT, "src", name + ".txt"), encoding="utf-8").read()
        u = parse(os.path.join(KIT, "data", name + ".txt"), src)
        for e in u["errors"]: print(f"  LỖI {name}: {e}")
        bad += len(u["errors"])
        out = {"book": book, "unit": un, "title_vi": u["title_vi"], "theory_html": theory_html(u["theory"]), "items": u["items"]}
        json.dump(out, open(os.path.join(KIT, "units", name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if "-q" not in sys.argv:
            for it in u["items"]:
                if it.get("ex_kit"): continue
                e = it["example"]["en"]; i = e.find("<b>"); w = e[:i].split()[-4:]; r = e[e.find("</b>") + 4:].split()[:4]
                print(f"   · {it['word']}: …{' '.join(w)} {e[i:e.find('</b>') + 4]} {' '.join(r)}…")
        print(f"{name}: {len(u['items'])} mục, {sum(1 for i in u['items'] if i.get('ex_kit'))} câu kit đặt, {len(u['errors'])} lỗi")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
