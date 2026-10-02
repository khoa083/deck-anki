# usage: fixg.py FILE word "G: text" [word "G: text"...]  — điền trường Ngữ pháp đang là "-" cho từ chỉ định
#        fixg.py FILE --auto                             — điền ghi chú từ loại/cấu tạo cho mọi mục còn "-"
import sys
p = sys.argv[1]; auto = "--auto" in sys.argv; m = dict(zip(sys.argv[2::2], sys.argv[3::2])) if not auto else {}
POS = {"n": "danh từ", "v": "động từ", "adj": "tính từ", "adv": "trạng từ", "prep": "giới từ", "conj": "liên từ", "det": "từ hạn định", "cl": "mệnh đề cố định", "phr": "cụm cố định", "excl": "thán từ", "pron": "đại từ"}
L = open(p, encoding="utf-8").read().split("\n")
for i, l in enumerate(L):
    f = l.split(" | ")
    if len(f) < 10 or l.startswith(("@", "##")): continue
    core = [j for j, x in enumerate(f) if not x.startswith(("exb=", "ex=", "sense="))]
    if len(core) < 10 or f[core[9]] != "-": continue
    if f[0] in m: f[core[9]] = m[f[0]]
    elif auto:
        w, pos = f[0], f[1].strip(); kind = POS.get(pos, pos)
        if "-" in w and " " not in w: note = f"G: {kind} ghép *{w.split('-')[0]}* + *{'-'.join(w.split('-')[1:])}*"
        elif " " in w: note = f"C: cụm {kind} cố định *{w}*" if pos in ("n", "adj", "adv") else f"G: {kind} nhiều từ *{w}*"
        else: note = f"G: {kind}"
        f[core[9]] = note
    else: continue
    L[i] = " | ".join(f)
open(p, "w", encoding="utf-8").write("\n".join(L))
