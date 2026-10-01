"""Ước lượng ví dụ có đặt trong ngữ cảnh sách không: tỉ lệ từ nội dung của example.en (bỏ headword, từ ngắn, từ chức năng) có trong src unit.
Dùng: python3 tools/context_score.py [unit ...]  → in mỗi unit: số ví dụ có điểm < 0.35 (nghi bối cảnh tự đặt) / tổng."""
import sys, os, re, json, glob
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOP = set("that this with from have been were they them their there what when where which while would could should about after before into over just only very really some because than then your yours ours also even still already".split())
def toks(s): return re.findall(r"[a-z]+", re.sub(r"<[^>]+>", " ", s).lower().replace("’", "'"))
def score(it, S):
    head = set(toks(it["word"]))
    ws = [w for w in toks(it["example"]["en"]) if len(w) > 3 and w not in STOP and w not in head]
    if not ws: return 1.0
    return sum(1 for w in ws if w in S or w.rstrip("s") in S or w[:-2] in S or w[:-3] in S) / len(ws)
names = sys.argv[1:] or sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(KIT, "units", "*.json")))
for n in names:
    u = json.load(open(os.path.join(KIT, "units", n + ".json"), encoding="utf-8"))
    S = set(toks(open(os.path.join(KIT, "src", n + ".txt"), encoding="utf-8").read()))
    low = [(round(score(it, S), 2), it["word"]) for it in u["items"] if score(it, S) < 0.35]
    print(f"{n}: {len(low):2d}/{len(u['items'])}", "; ".join(f"{w} {x}" for x, w in low[:6]))
