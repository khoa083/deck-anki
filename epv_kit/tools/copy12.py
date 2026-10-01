"""In ra các cụm >=12 từ liên tiếp trong theory_html trùng src (giúp sửa cảnh báo check)."""
import json, re, sys
u = sys.argv[1]
t = re.sub(r'<[^>]+>', ' ', json.load(open(f'units/{u}.json'))['theory_html']).lower()
sw = ' '.join(re.findall(r"[a-z’']+", open(f'src/{u}.txt').read().lower()))
w = re.findall(r"[a-z’']+", t)
for i in range(len(w) - 11):
    g = ' '.join(w[i:i + 12])
    if g in sw: print(g)
