# epv_kit – English Phrasal Verbs in Use (Advanced + Intermediate)
Bắt đầu: đọc `PROMPT.md`. Dán PROMPT.md vào chat mới + upload `epv_kit.zip` và 2 PDF sách (bản 2).

| Đường dẫn | Nội dung |
|---|---|
| `PROMPT.md` | quy trình, luật chống sai lệch, quyết định mặc định |
| `STYLE_GUIDE.md` | đặc tả từng field, thẻ mẫu, thuật ngữ tiếng Việt |
| `implementation-notes.md` | kết quả kiểm chứng kit với sách, tiến độ, Todo |
| `epv.py` | doctor · selftest · status · check · demo · **audio** · build · verify |
| `media/` | audio Phát âm của thẻ mới (Kokoro TTS, giọng Anh–Anh) |
| `tools/make_audio.py` | tạo audio; model tải về `~/.cache/epv_tts/` (không nằm trong zip) |
| `base/` | deck demo (Advanced 1–16 bản 1, 347 thẻ + audio) |
| `src/` | nguồn từng unit trích từ sách (130 file) |
| `tools/` | books.json, build_deck.py, common.py, extract_src.py, page_img.py, ocr_int.sh |
| `gen/`, `units/` | script sinh unit / JSON unit (bản gốc để build) |
