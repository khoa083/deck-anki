#!/usr/bin/env python3
"""Compile data/<book>_uNNN.txt -> units/<book>_uNNN.json (theory HTML theo deck mẫu EGU + danh sách MCQ).

Dùng:  python3 tools/compile.py BOOK U [U…]     (không có U -> mọi file data của BOOK)

Định dạng data (mỗi dòng song ngữ dùng ‖ ngăn EN và VI; VI = "=" nghĩa là giống EN):
  @title_vi: tên bài tiếng Việt
  @egu: 1-4,19,25                         -> (sup) unit EGU Intermediate liên quan: lý thuyết lấy từ deck mẫu khi build
  @theory
  ## A | EN heading | VI heading          -> mục A/B/C… (heading có thể rỗng)
  EN ‖ VI                                 -> đoạn văn
  - EN ‖ VI                               -> ví dụ (gộp thành <ul>)
  |! ô | ô | ô                            -> hàng tiêu đề bảng (ô song ngữ: "EN ‖ VI")
  | ô | ô | ô                             -> hàng bảng
  @rules
  KEY: EN ‖ VI                            -> quy tắc dùng trong "Giải thích"
  @mcq
  RULE[,RULE] | câu có ___ | đúng | sai1 | sai2 | dịch VI với [phần đậm] | Điểm ngữ pháp (VI)
Inline: **đậm**, *nghiêng*. Nhiều chỗ trống: đáp án nối bằng " … ". Đáp án "–" = không điền gì.
"""
import sys, os, re, json, glob, html
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
BOOKS = json.load(open(os.path.join(HERE, "books.json"), encoding="utf-8"))
P = '<p style="text-align: justify;">'
TD = '<td style="padding: 8px;">'
TH = '<th style="padding: 8px;">'
EMPTY = ("–", "-", "—")


def inline(s):
    s = html.escape(s.strip(), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    return s


def bi(line, where):
    if "‖" not in line: raise ValueError(f"{where}: thiếu ‖ – {line[:70]}")
    en, vi = (x.strip() for x in line.split("‖", 1))
    if not en or not vi: raise ValueError(f"{where}: EN hoặc VI rỗng – {line[:70]}")
    return en, (en if vi == "=" else vi)


def cell(c):
    if "‖" in c:
        en, vi = bi(c, "bảng")
        return f"{inline(en)}<br><i>{inline(vi)}</i>" if en != vi else inline(en)
    return inline(c)


def theory_html(lines, where):
    out, ul, tab = [], [], []

    def flush():
        if ul:
            out.append("<ul>\n" + "".join(f"  <li>\n    {P}{inline(e)}</p>\n    {P}<i>{inline(v)}</i></p>\n  </li>\n" for e, v in ul) + "</ul>")
            ul.clear()
        if tab:
            head = [r for h, r in tab if h]; body = [r for h, r in tab if not h]
            t = '<table border="1" style="border-collapse: collapse; border-color: black; padding: 8px; margin: 6px 0;">\n'
            if head: t += "  <thead>\n" + "".join("    <tr>" + "".join(f"{TH}{cell(c)}</th>" for c in r) + "</tr>\n" for r in head) + "  </thead>\n"
            t += "  <tbody>\n" + "".join("    <tr>" + "".join(f"{TD}{cell(c)}</td>" for c in r) + "</tr>\n" for r in body) + "  </tbody>\n</table>"
            out.append(t); tab.clear()

    for ln in lines:
        s = ln.strip()
        if not s: continue
        if s.startswith("|"):
            if ul: flush()
            hdr = s.startswith("|!"); cells = [c.strip() for c in s[2 if hdr else 1:].split(" | ")]
            tab.append((hdr, cells)); continue
        if s.startswith("- "):
            if tab: flush()
            ul.append(bi(s[2:], where)); continue
        flush()
        if s.startswith("## "):
            parts = [x.strip() for x in s[3:].split("|")]
            lab, en, vi = (parts + ["", "", ""])[:3]
            en_t = f"{lab}. {en}" if en else lab; vi_t = f"{lab}. {vi}" if vi else lab
            out.append(f"{P}<b>{inline(en_t)}</b></p>" + (f"\n{P}<i>{inline(vi_t)}</i></p>" if vi_t != en_t else ""))
            continue
        en, vi = bi(s, where)
        out.append(f"{P}{inline(en)}</p>\n{P}<i>{inline(vi)}</i></p>")
    flush()
    return "\n\n".join(out)


def fill(q, ans):
    parts = q.split("___"); n = len(parts) - 1
    vals = [a.strip() for a in ans.split(" … ")] if n > 1 else [ans.strip()]
    if len(vals) != n: raise ValueError(f"{n} chỗ trống nhưng đáp án có {len(vals)} phần: {q} / {ans}")
    out = parts[0]
    for v, nxt in zip(vals, parts[1:]):
        if v in EMPTY: out = out.rstrip(" ") + " " + nxt.lstrip(" ")
        else:
            if v[:1] in "’'" and out.endswith(" "): out = out[:-1]
            out += f"**{v}**" + nxt
    out = re.sub(r"\s{2,}", " ", out).strip()
    if q.startswith("___") and vals[0] in EMPTY: out = out[:1].upper() + out[1:]
    return out


def parse_units(s, where):
    out = []
    for p in s.replace(" ", "").split(","):
        if not p: continue
        a, _, b = p.replace("–", "-").partition("-")
        if not a.isdigit() or (b and not b.isdigit()): raise ValueError(f"{where}: @egu sai – {s}")
        out += range(int(a), int(b or a) + 1)
    return sorted(set(out))


def compile_file(book, un):
    fn = os.path.join(KIT, "data", f"{book}_u{un:03d}.txt"); where = os.path.basename(fn)
    meta, sect, buf = {}, None, {"theory": [], "rules": [], "mcq": []}
    for i, ln in enumerate(open(fn, encoding="utf-8").read().splitlines(), 1):
        if ln.startswith("@title_vi:"): meta["title_vi"] = ln.split(":", 1)[1].strip(); continue
        if ln.startswith("@egu:"): meta["egu"] = parse_units(ln.split(":", 1)[1], where); continue
        if ln.strip() in ("@theory", "@rules", "@mcq"): sect = ln.strip()[1:]; continue
        if ln.strip().startswith("#!"): continue          # chú thích
        if sect: buf[sect].append(ln)
    rules = {}
    for r in buf["rules"]:
        if not r.strip(): continue
        k, rest = r.split(":", 1); rules[k.strip()] = bi(rest, f"{where} rule {k}")
    mcq, seen = [], set()
    for ln in buf["mcq"]:
        if not ln.strip(): continue
        f = [x.strip() for x in ln.split(" | ")]
        if len(f) != 7: raise ValueError(f"{where}: MCQ cần 7 cột, có {len(f)} – {ln[:80]}")
        keys, q, a, b, c, vi, note = f
        if "___" not in q: raise ValueError(f"{where}: thiếu ___ – {q}")
        if len({a, b, c}) < 3: raise ValueError(f"{where}: đáp án trùng – {q}")
        if (q, a) in seen: raise ValueError(f"{where}: MCQ trùng – {q}")
        seen.add((q, a))
        expl = []
        for k in keys.split(","):
            k = k.strip()
            if k not in rules: raise ValueError(f"{where}: rule '{k}' chưa khai báo – {q}")
            expl.append(f"{inline(rules[k][0])}<br><i>{inline(rules[k][1])}</i>")
        if "[" not in vi: raise ValueError(f"{where}: bản dịch thiếu [phần đậm] – {vi}")
        mcq.append({"question": inline(q), "a": inline(a), "b": inline(b), "c": inline(c),
                    "full": inline(fill(q, a)),
                    "vi": "<i>" + inline(vi).replace("[", "<b>").replace("]", "</b>") + "</i>",
                    "expl": "<br>".join(expl) + f"<br><b>Điểm ngữ pháp</b>: {inline(note)}", "key": f"{q}|{a}"})
    if not meta.get("title_vi"): raise ValueError(f"{where}: thiếu @title_vi")
    u = {"book": book, "unit": un, "title_en": BOOKS[book]["units"][str(un)]["title"], "title_vi": meta["title_vi"],
         "theory_html": theory_html(buf["theory"], where), "mcq": mcq}
    if meta.get("egu"): u["egu_units"] = meta["egu"]
    os.makedirs(os.path.join(KIT, "units"), exist_ok=True)
    json.dump(u, open(os.path.join(KIT, "units", f"{book}_u{un:03d}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return u


def main():
    book = sys.argv[1]
    uns = [int(x) for x in sys.argv[2:]] or sorted(int(re.search(r"_u(\d+)\.txt$", f).group(1)) for f in glob.glob(os.path.join(KIT, "data", f"{book}_u*.txt")))
    bad = 0
    for un in uns:
        try:
            u = compile_file(book, un); print(f"  {book}_u{un:03d}: {len(u['mcq'])} MCQ")
        except Exception as e:
            bad += 1; print(f"  LỖI {book}_u{un:03d}: {e}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
