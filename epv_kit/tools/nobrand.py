"""Bỏ toàn bộ chữ "Anki Support Vietnam" khỏi deck (yêu cầu người dùng):
link trong template note type, giá trị trường Nguồn ("AnkiSupportVietnam") và mô tả deck."""
import re
BRAND = re.compile(r"anki\s*support\s*viet\s*nam", re.I)
LINK_DIV = re.compile(r"<div\b[^>]*>\s*<a\b[^>]*>\s*Anki\s*Support\s*Vietnam\s*</a>\s*</div>", re.I | re.S)
LINK = re.compile(r"<a\b[^>]*>\s*Anki\s*Support\s*Vietnam\s*</a>", re.I | re.S)


def strip_brand(col):
    st = {"templates": 0, "fields": 0, "decks": 0}
    for m in col.models.all():
        ch = False
        for t in m["tmpls"]:
            for side in ("qfmt", "afmt"):
                s = LINK.sub("", LINK_DIV.sub("", t[side]))
                if s != t[side]: t[side] = s; ch = True; st["templates"] += 1
        if ch: col.models.update_dict(m)
    for nid in col.find_notes(""):
        n = col.get_note(nid); ch = False
        for k, v in n.items():
            if BRAND.search(v):
                n[k] = BRAND.sub("", v).strip(); ch = True
        if ch: col.update_note(n); st["fields"] += 1
    for d in col.decks.all():
        if BRAND.search(d.get("desc", "")):
            d["desc"] = BRAND.sub("", d["desc"]); col.decks.save(d); st["decks"] += 1
    return st


def brand_left(col):
    """Số chỗ còn sót chữ thương hiệu (dùng trong verify)."""
    left = 0
    for m in col.models.all():
        for t in m["tmpls"]: left += len(BRAND.findall(t["qfmt"] + t["afmt"]))
        left += len(BRAND.findall(m["css"]))
    for nid in col.find_notes(""):
        left += sum(1 for _, v in col.get_note(nid).items() if BRAND.search(v))
    left += sum(1 for d in col.decks.all() if BRAND.search(d.get("desc", "")))
    return left
