"""In ra đoạn dài nhất của theory_html trùng src (cùng thuật toán với epv.py check, §3)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import epv
u = sys.argv[1]
d = json.load(open(f'units/{u}.json'))
body = epv.SUM_RE.sub("", d["theory_html"])
A = epv.toks(epv.strip(body)); T = " " + " ".join(epv.toks(epv.src(d["book"], d["unit"]))) + " "
for i in range(len(A) - 11):
    if " " + " ".join(A[i:i + 12]) + " " in T: print(" ".join(A[i:i + 14]))
