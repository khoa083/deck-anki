"""Tạo audio cho field *Phát âm* (đọc headword) bằng Kokoro TTS offline, giọng Anh–Anh.

Dùng:  python3 epv.py audio [unit ...]      (mặc định: mọi units/*.json)
- Model tải 1 lần từ GitHub release của kokoro-onnx (domain github.com được phép) vào ~/.cache/epv_tts/.
- File: media/epv_<book>_u<NN>_<slug>.mp3 (mono 24 kHz 96 kbps, cùng định dạng audio demo).
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
# Thêm vào config.json "tts_phonemes". Kiểm bằng `python3 epv.py audio --report` (in phoneme TTS cạnh IPA của thẻ).
PH = CFG.get("tts_phonemes", {})

def audio_name(book, unit, item):
    w = item["word"].strip().lower(); s = item.get("sense", "").strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", w + ("-" + s if s else "")).strip("-")
    return f"epv_{book}_u{unit:02d}_{slug}.mp3"

def spoken(word):
    """Văn bản đọc = headword (bỏ chú thích trong ngoặc, giữ somebody/something như demo)."""
    return re.sub(r"\s*\(.*?\)", "", word).replace("/", " or ").strip()

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
            if force or not os.path.exists(fn) or it["word"] in PH: todo.append((fn, spoken(it["word"]), PH.get(it["word"])))
    if not todo: print("audio: đủ, không cần tạo"); return
    import soundfile as sf
    k = model(); voice = CFG.get("tts_voice", "bm_george"); speed = CFG.get("tts_speed", 0.95)
    for fn, text, ph in todo:
        s, sr = k.create(ph or text, voice=voice, speed=speed, lang="en-gb", is_phonemes=bool(ph))
        b = io.BytesIO(); sf.write(b, s, sr, format="WAV")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "-", "-ac", "1", "-ar", "24000", "-b:a", "96k", fn],
                       input=b.getvalue(), check=True)
    print(f"audio: tạo {len(todo)} file ({voice}) -> media/")

def report():
    """In phoneme TTS cạnh IPA thẻ để soát trọng âm/nguyên âm sai."""
    from kokoro_onnx.tokenizer import Tokenizer
    t = Tokenizer()
    for p in sorted(glob.glob(os.path.join(KIT, "units", "*.json"))):
        u = json.load(open(p, encoding="utf-8"))
        for it in u["items"]:
            ph = PH.get(it["word"]) or t.phonemize(spoken(it["word"]), "en-gb")
            print(f'{u["book"]}_u{u["unit"]:02d}  {spoken(it["word"]):34s} TTS {ph:34s} IPA {it["ipa"]}')

if __name__ == "__main__":
    main(sys.argv[1:])
