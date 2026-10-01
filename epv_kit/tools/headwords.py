"""In mọi headword đã có (demo + units/*.json) để kiểm trùng nhanh: python3 tools/headwords.py [từ khoá ...]"""
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import epv
rows = [(d["word"], f"demo u{d['unit']}", "") for d in epv.demo_notes()]
for f in sorted(glob.glob(os.path.join(epv.KIT, "units", "*.json"))):
    u = json.load(open(f, encoding="utf-8"))
    rows += [(it["word"], f"{u['book']} u{u['unit']}", it.get("sense", "")) for it in u["items"]]
keys = [k.lower() for k in sys.argv[1:]]
for w, where, s in rows:
    if not keys or any(k in w.lower() for k in keys): print(f"{w:40s} {where:10s} {s}")
