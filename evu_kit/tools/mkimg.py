"""Cắt ảnh minh họa từ PDF sách gốc theo tools/images.json -> img/<file> (JPEG, rộng ~900px)."""
import json, os, io, pymupdf
from PIL import Image
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def main():
    os.makedirs(os.path.join(KIT, "img"), exist_ok=True)
    docs = {}
    for s in json.load(open(os.path.join(KIT, "tools", "images.json"), encoding="utf-8")):
        out = os.path.join(KIT, "img", s["file"])
        if os.path.exists(out): continue
        d = docs.setdefault(s["book"], pymupdf.open(os.path.join(KIT, "books", s["book"] + ".pdf")))
        pg = d[s["page"] - 1]; r = pg.rect
        clip = pymupdf.Rect(r.x0 + s["clip"][0] * r.width, r.y0 + s["clip"][1] * r.height,
                            r.x0 + s["clip"][2] * r.width, r.y0 + s["clip"][3] * r.height) if s["clip"] else r
        pix = pg.get_pixmap(dpi=int(72 * 900 / clip.width), clip=clip)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im.save(out, "JPEG", quality=62, optimize=True)
    print("ảnh:", len(os.listdir(os.path.join(KIT, "img"))))
if __name__ == "__main__": main()
