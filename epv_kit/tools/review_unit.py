#!/usr/bin/env python3
"""Rà soát KỸ một unit trước khi chuyển unit khác (bổ sung cho `epv.py check`).

Dùng:  python3 tools/review_unit.py adv_u46 [--render]
 1. In từng mục dạng đọc được, kèm dòng Mini dictionary tương ứng → đối chiếu bằng mắt với src/ảnh trang.
 2. Audio: file tồn tại, ffprobe đọc được, độ dài hợp lý (0.4–6 s), có tiếng (mean_volume > −40 dB), không trùng nội dung (md5) với mục khác.
 3. Phoneme TTS cạnh IPA của thẻ (soát trọng âm/nguyên âm).
 4. --render: đọc out/EPV_full.apkg (phải build trước), render cả 2 thẻ của mọi note trong unit:
    không còn {{…}}, có [sound:…] trỏ tới file có thật trong media, có headword, có lý thuyết.
"""
import sys, os, re, json, subprocess, hashlib, html, tempfile
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(KIT, "tools"))
from make_audio import audio_name, spoken, PH

def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def main(name, render):
    u = json.load(open(os.path.join(KIT, "units", name + ".json"), encoding="utf-8"))
    src = open(os.path.join(KIT, "src", f"{name}.txt"), encoding="utf-8").read()
    md = re.search(r"### MINI DICTIONARY.*?\n(.*)", src, re.S); md = md.group(1).splitlines() if md else []
    probs, md5 = [], {}
    from kokoro_onnx.tokenizer import Tokenizer
    tok = Tokenizer()
    for k, it in enumerate(u["items"], 1):
        w = it["word"]; core = re.sub(r"\b(somebody|something|somewhere|yourself)\b", "", w).replace("/", " ").split()
        hit = [l for l in md if core and all(c.lower()[:4] in l.lower() for c in core[:2])]
        print(f"\n#{k} {w}" + (f"  [sense: {it['sense']}]" if it.get("sense") else "") + f"  ({it['pos']}, {it['register']})  {it['ipa']}")
        print("  MINI:", " | ".join(h.strip("- ") for h in hit) or "— (không thấy dòng Mini dictionary khớp – kiểm tay)")
        print("  def_en:", it["def_en"]); print("  def_vi:", it["def_vi"], "| gloss:", it["gloss_vi"])
        print("  ex_en :", strip(it["example"]["en"])); print("  ex_vi :", strip(it["example"]["vi"]))
        print("  gram  :", strip(it["grammar_vi"]))
        print("  syn/ant:", ", ".join(s["text"] for s in it["synonyms"]), "/", ", ".join(s["text"] for s in it["antonyms"]))
        fn = os.path.join(KIT, "media", audio_name(u["book"], u["unit"], it))
        if not os.path.exists(fn): probs.append(f"{w}: THIẾU audio"); continue
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,sample_rate,channels",
                            "-of", "json", fn], capture_output=True, text=True)
        try:
            info = json.loads(r.stdout); dur = float(info["format"]["duration"]); st = info["streams"][0]
            ok = 0.4 <= dur <= 6 and st["codec_name"] == "mp3"
            print(f"  audio : {os.path.basename(fn)} {dur:.2f}s {st['codec_name']} {st['sample_rate']}Hz ch{st['channels']}" + ("" if ok else "  <-- BẤT THƯỜNG"))
            if not ok: probs.append(f"{w}: audio bất thường ({dur:.2f}s)")
        except Exception as e: probs.append(f"{w}: ffprobe lỗi {e}")
        vd = subprocess.run(["ffmpeg", "-hide_banner", "-i", fn, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
        mv = re.search(r"mean_volume: (-?[\d.]+) dB", vd)
        if not mv or float(mv.group(1)) < -40: probs.append(f"{w}: audio gần như câm ({mv.group(1) if mv else '?'} dB)")
        h = hashlib.md5(open(fn, "rb").read()).hexdigest()
        if h in md5: probs.append(f"{w}: audio trùng nội dung với {md5[h]}")
        md5[h] = w
        print(f"  TTS   : {PH.get(w) or tok.phonemize(spoken(w), 'en-gb')}" + ("   (tts_phonemes)" if w in PH else ""))
    if render: probs += render_check(u)
    print("\n== VẤN ĐỀ:", probs or "không có")

def render_check(u):
    from anki.collection import Collection, ImportAnkiPackageRequest, ImportAnkiPackageOptions
    d = tempfile.mkdtemp(); col = Collection(os.path.join(d, "t.anki2"))
    col.import_anki_package(ImportAnkiPackageRequest(package_path=os.path.join(KIT, "out", "EPV_full.apkg"),
                            options=ImportAnkiPackageOptions(with_scheduling=False, with_deck_configs=True)))
    tag = f"EPV::{u['book']}::u{u['unit']:02d}"; P = []; n_cards = 0
    words = {it["word"] for it in u["items"]}; seen = set()
    for nid in col.find_notes(f"tag:{tag}"):
        n = col.get_note(nid); w = strip(n.fields[0])
        for c in n.cards():
            n_cards += 1; q, a = c.question(), c.answer()
            if "{{" in q + a or "Unknown field" in a: P.append(f"render lỗi: {w} card {c.ord}")
        if len(n.fields) > 11:      # note từ vựng
            seen.add(w)
            m = re.search(r"\[sound:([^\]]+)\]", n.fields[11])
            if not m or not os.path.exists(os.path.join(col.media.dir(), m.group(1))): P.append(f"{w}: audio không có trong media của gói")
            if len(strip(n.fields[12])) < 300: P.append(f"{w}: thiếu lý thuyết trong thẻ")
            decks = {col.decks.name(c.did).split("::")[2] for c in n.cards()}
            if len(decks) != 2: P.append(f"{w}: 2 thẻ không nằm ở 2 deck con (nhìn/nghe): {decks}")
    miss = {strip(x) for x in words} - seen
    if miss: P.append(f"thiếu note trong gói: {miss}")
    print(f"\n== RENDER: {len(col.find_notes(f'tag:{tag}'))} note, {n_cards} thẻ của {tag} đã render")
    col.close(); return P

if __name__ == "__main__":
    main(sys.argv[1], "--render" in sys.argv)
