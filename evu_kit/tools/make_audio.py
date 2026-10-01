"""Tạo audio cho field *Phát âm* (đọc headword) bằng Kokoro TTS offline, giọng Anh–Anh.

Dùng:  python3 evu.py audio [unit ...]      (mặc định: mọi units/*.json)
- Model tải 1 lần từ GitHub release của kokoro-onnx (domain github.com được phép) vào ~/.cache/epv_tts/.
- File: media/epv_<book>_u<NN>_<slug>.mp3 (mono 24 kHz 64 kbps).
- Đã có file thì bỏ qua (thêm --force để tạo lại). Build sẽ báo LỖI nếu mục nào thiếu audio.
"""
import os, re, sys, json, glob, io, subprocess, urllib.request
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(KIT, "config.json"), encoding="utf-8"))
CACHE = os.path.expanduser("~/.cache/epv_tts")
URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
FILES = ("kokoro-v1.0.onnx", "voices-v1.0.bin")
MEDIA = os.path.join(KIT, "media")
# Sửa phát âm khi TTS đọc sai (trọng âm danh từ thay vì động từ, BATH /æ/ thay vì /ɑː/…): headword -> phoneme Kokoro.
# Thêm vào config.json "tts_phonemes". Kiểm bằng `python3 evu.py audio --report` (in phoneme TTS cạnh IPA của thẻ).
PH = CFG.get("tts_phonemes", {})

def audio_name(book, unit, item):
    w = item["word"].strip().lower(); s = item.get("sense", "").strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", w + ("-" + s if s else "")).strip("-")
    return f"evu_{book}_u{unit:02d}_{slug}.mp3"

def spoken(word):
    """Văn bản đọc = headword (bỏ chú thích trong ngoặc, giữ somebody/something như demo)."""
    return re.sub(r"\s*\(.*?\)", "", word).replace("/", " or ").strip()

# Từ nhóm BATH (chuẩn Anh /ɑː/, Kokoro en-gb hay đọc /æ/ = 'a'). Tự sửa khi headword chứa các từ này và chưa có tts_phonemes.
BATH = {"after", "afterwards", "ask", "asks", "asked", "asking", "pass", "passed", "passing", "past", "last", "fast", "class", "glass",
        "grass", "path", "bath", "laugh", "dance", "chance", "plant", "branch", "answer", "cast", "castle", "blast", "grasp", "staff",
        "can't", "aunt", "master", "vast", "draft", "craft", "advance", "demand", "example", "rather", "half", "calm", "father"}
_tok = None
def auto_phonemes(text):
    """Trả về chuỗi phoneme đã sửa BATH nếu text có từ nhóm BATH, ngược lại None (để Kokoro tự xử lý)."""
    global _tok
    ws = text.split()
    if not any(w.lower().strip(".,!?…") in BATH for w in ws): return None
    if _tok is None:
        from kokoro_onnx.tokenizer import Tokenizer
        _tok = Tokenizer()
    out = []
    for w in ws:
        ph = _tok.phonemize(w, "en-gb")
        if w.lower().strip(".,!?…") in BATH: ph = re.sub(r"a(?=[fsθnmlː]|$)", "ɑː", ph, count=1).replace("ɑːː", "ɑː")
        out.append(ph)
    return " ".join(out)

def noun_stress(word):
    """Danh từ phrasal có gạch nối (break-in, mix-up…): trọng âm ở phần đầu (sách: a BREAK-in) – bỏ trọng âm phần sau."""
    global _tok
    if _tok is None:
        from kokoro_onnx.tokenizer import Tokenizer
        _tok = Tokenizer()
    a, b = word.split("-", 1)
    return _tok.phonemize(a, "en-gb") + _tok.phonemize(b.replace("-", " "), "en-gb").replace("ˈ", "").replace("ˌ", "")

def model():
    os.makedirs(CACHE, exist_ok=True)
    for f in FILES:
        p = os.path.join(CACHE, f)
        if not os.path.exists(p) or os.path.getsize(p) < 1_000_000:
            print("tải", f, "…"); urllib.request.urlretrieve(URL + f, p)
    from kokoro_onnx import Kokoro
    return Kokoro(*(os.path.join(CACHE, f) for f in FILES))

def main(args):
    if "--report" in args: return report()
    force = "--force" in args; names = [a.replace(".json", "") for a in args if not a.startswith("--")]
    paths = [os.path.join(KIT, "units", n + ".json") for n in names] or sorted(glob.glob(os.path.join(KIT, "units", "*.json")))
    os.makedirs(MEDIA, exist_ok=True)
    todo = []
    for p in paths:
        u = json.load(open(p, encoding="utf-8"))
        for it in u["items"]:
            fn = os.path.join(MEDIA, audio_name(u["book"], u["unit"], it))
            ph = PH.get(it["word"]) or auto_phonemes(spoken(it["word"]))
            if not ph and it.get("pos") in ("noun", "n.") and "-" in it["word"] and " " not in it["word"].strip(): ph = noun_stress(it["word"])
            if force or not os.path.exists(fn) or it["word"] in PH: todo.append((fn, spoken(it["word"]), ph))
    if not todo: print("audio: đủ, không cần tạo"); return
    import soundfile as sf
    k = model(); voice = CFG.get("tts_voice", "bm_george"); speed = CFG.get("tts_speed", 0.95)
    for fn, text, ph in todo:
        s, sr = k.create(ph or text, voice=voice, speed=speed, lang="en-gb", is_phonemes=bool(ph))
        b = io.BytesIO(); sf.write(b, s, sr, format="WAV")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "-", "-ac", "1", "-ar", "24000", "-b:a", "64k", fn],
                       input=b.getvalue(), check=True)
    print(f"audio: tạo {len(todo)} file ({voice}) -> media/")

def report():
    """In phoneme TTS cạnh IPA thẻ để soát trọng âm/nguyên âm sai."""
    from kokoro_onnx.tokenizer import Tokenizer
    t = Tokenizer()
    for p in sorted(glob.glob(os.path.join(KIT, "units", "*.json"))):
        u = json.load(open(p, encoding="utf-8"))
        for it in u["items"]:
            ph = PH.get(it["word"]) or auto_phonemes(spoken(it["word"])) or (noun_stress(it["word"]) if it.get("pos") in ("noun", "n.") and "-" in it["word"] and " " not in it["word"].strip() else None) or t.phonemize(spoken(it["word"]), "en-gb")
            print(f'{u["book"]}_u{u["unit"]:02d}  {spoken(it["word"]):34s} TTS {ph:34s} IPA {it["ipa"]}')

if __name__ == "__main__":
    main(sys.argv[1:])
