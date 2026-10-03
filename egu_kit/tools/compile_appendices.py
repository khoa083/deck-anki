#!/usr/bin/env python3
"""Compile authored appendix study notes from data/ess_appendices.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
src = os.path.join(KIT, "data", "ess_appendices.json")
out_dir = os.path.join(KIT, "units")
items = json.load(open(src, encoding="utf-8"))
for item in items:
    item["book"] = "ess"
    target = os.path.join(out_dir, f"ess_a{item['n']:02d}.json")
    json.dump(item, open(target, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  ess_a{item['n']:02d}: {item['title_en']}")
print(f"Compiled {len(items)} appendix notes")
