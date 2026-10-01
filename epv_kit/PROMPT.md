# PROMPT – Làm tiếp deck *English Phrasal Verbs in Use* (Advanced + Intermediate)

> Dán toàn bộ file này vào chat mới, kèm 3 file: `epv_kit.zip`, PDF *Advanced* (2nd ed.), PDF *Intermediate* (2nd ed.).
> Trả lời tôi bằng **tiếng Việt**.

## 0. Vai trò và mục tiêu
Bạn làm tiếp bộ deck Anki song ngữ Anh–Việt từ 2 cuốn *English Phrasal Verbs in Use* **2nd edition** (Advanced 60 unit, Intermediate 70 unit),
dựa trên deck demo có sẵn (Advanced unit 1–15). **Sách PDF là nguồn sự thật duy nhất.** Chính xác và trung thành với sách quan trọng hơn làm nhiều.

## 1. Chuẩn bị (lượt đầu tiên)
```bash
cd /home/claude && unzip -o -q /mnt/user-data/uploads/epv_kit.zip && cd epv_kit
pip install anki pymupdf kokoro-onnx soundfile --break-system-packages -q
mkdir -p books && cp /mnt/user-data/uploads/*Advanced*.pdf books/adv.pdf && cp /mnt/user-data/uploads/*Intermediate*.pdf books/int.pdf
python3 epv.py doctor && python3 epv.py selftest && python3 epv.py status
```
Đọc hết: `PROMPT.md` (file này), `STYLE_GUIDE.md`, `implementation-notes.md`. Xem 3 thẻ demo mẫu: `python3 epv.py demo adv 2`.
Nếu `selftest` báo CÓ VẤN ĐỀ → dừng, báo tôi, không làm tiếp.

## 2. Sự thật đã kiểm chứng (đừng làm lại, đừng đoán khác)
- **Hai sách là bản 2.** Advanced PDF có lớp chữ; Intermediate PDF là **bản scan** → `src/int_*.txt` là text OCR (có lỗi) và **không có danh sách in đậm**.
- Trang: Advanced unit n = PDF index 0-based `7+2n` (lý thuyết) / `8+2n` (bài tập). Intermediate unit n = trang PDF 1-based `6+2n` / `7+2n`.
  Tên 130 unit và phân mục trong `tools/books.json` đã đối chiếu với từng trang sách.
- **Demo theo bản 1**: demo unit 9 *New phrasal verbs* không có ở bản 2; demo unit 10–16 = bản 2 unit 9–15 (đã chứng minh bằng độ trùng nội dung 69–81%).
  Build tự đổi số: deck, STT, tiêu đề "Unit N" trong lý thuyết; *New phrasal verbs* giữ làm deck bổ sung `08x-…` (STT `B1-09`, tiêu đề "Unit 9 (bản 1)").
- 4 thẻ demo chỉ có ở bản 1 được gắn tag `EPV::demo_ban1` (không xoá); 3 thẻ demo sửa dạng theo bản 2 (`hit/bear/call upon` → `… on`).
- Mỗi `src/<book>_uNN.txt` có: BOLD (chỉ Advanced) · LEFT PAGE · RIGHT PAGE · KEY (đáp án) · **MINI DICTIONARY** (định nghĩa chính thức của sách cho unit đó).

## 3. Quyết định mặc định (tôi có thể đổi bằng 1 câu)
| # | Quyết định | Mặc định | Đổi thành |
|---|---|---|---|
| D1 | Thứ tự làm | Advanced 16→60, rồi bổ sung demo (Adv 1–15), rồi Intermediate 1→70 | "làm Intermediate trước" |
| D2 | IPA | Chuẩn Anh cho mọi thẻ (đổi luôn IPA Mỹ của demo) | `config.json: "ipa_style": "keep"` |
| D3 | Cấu trúc deck | 1 deck gốc `English Phrasal Verbs in Use` → `Advanced` / `Intermediate` | – |
| D4 | Thẻ demo chỉ có ở bản 1 | Giữ + tag `EPV::demo_ban1` | "xoá" |
| D5 | Audio | **BẮT BUỘC** mỗi thẻ mới có audio ở field *Phát âm* (đọc headword): Kokoro TTS offline, giọng Anh–Anh nam `bm_george` (config `tts_voice`). `python3 epv.py audio` (model tự tải 1 lần từ GitHub). Build báo LỖI nếu thiếu. | `tts_voice` |
| D6 | Chọn mục cho mỗi unit | Mọi phrasal verb / danh từ / tính từ phrasal mà **Mini dictionary** gán cho unit + cụm in đậm được dạy trên trang lý thuyết. Mỗi nghĩa khác nhau = 1 thẻ (`sense`) | – |

## 4. Quy trình mỗi lượt (tôi nói "tiếp tục" = làm 5 unit kế tiếp)
Cho **từng unit**:
1. Đọc `src/<book>_uNN.txt` toàn bộ. **Intermediate: bắt buộc xem ảnh trang** `python3 tools/page_img.py int NN both` rồi mở PNG bằng công cụ xem ảnh, sửa mọi lỗi OCR theo ảnh. Advanced: xem ảnh khi bảng/khung bị trộn.
2. Lập danh sách mục = Mini dictionary của unit (+ cụm in đậm được dạy). Kiểm trùng: `python3 epv.py status`, và `check` sẽ báo trùng với demo / unit khác.
3. Viết `gen/<book>_uNN.py` theo `STYLE_GUIDE.md` **§0 chế độ bám sách – diễn giải** (lý thuyết diễn giải sát từng mục của sách; ví dụ đặt trong ngữ cảnh sách; collocation/lỗi thường gặp chỉ lấy từ unit; mẫu: `gen/adv_u16.py`…) → `python3 gen/<book>_uNN.py`.
3b. **Audio (bắt buộc):** `python3 epv.py audio` → tạo `media/*.mp3` cho mục mới; `python3 epv.py audio --report` → soát phoneme TTS cạnh IPA thẻ, chỗ đọc sai trọng âm/nguyên âm (vd. động từ *impact*, *attribute*; BATH /ɑː/) thêm vào `config.json` → `tts_phonemes` rồi chạy lại `audio`.
4. `python3 epv.py check <book>_uNN` → sửa **hết LỖI** (thiếu audio = LỖI); đọc từng cảnh báo và xử lý:
   ví dụ/def_en/lý thuyết trùng sách → diễn đạt lại; collocation không có trong src → thay bằng cụm của sách; Mini dictionary còn mục chưa có thẻ → thêm hoặc ghi lý do bỏ (vd. đã có trong demo cùng nghĩa).
5. Sau 5 unit: `python3 epv.py build && python3 epv.py verify` (phải thấy `audio thẻ mới: N/N – đủ`), cập nhật `implementation-notes.md` (tiến độ, Deviations, Todo for human),
   đóng gói: `cd /home/claude && zip -qr /mnt/user-data/outputs/epv_kit.zip epv_kit -x "epv_kit/books/*" "epv_kit/out/*" && cp epv_kit/out/EPV_full.apkg epv_kit/implementation-notes.md /mnt/user-data/outputs/`, rồi `present_files` **cả 3 file: `EPV_full.apkg`, `epv_kit.zip`, `implementation-notes.md`** (bắt buộc mỗi lượt – người dùng kiểm tra notes riêng, không mở trong zip).

## 5. Luật chống sai lệch (quan trọng nhất)
- **Không bịa.** Headword, định nghĩa, ví dụ, nhãn văn phong, ngữ pháp phải có căn cứ trong src/ảnh trang của **chính unit đó**. Không lấy nghĩa ở unit khác hay từ trí nhớ chung rồi ghi như thể sách dạy.
- **Bám sách 100% nhưng không chép nguyên văn** (lý thuyết, định nghĩa, ví dụ). `def_en` = nghĩa Mini dictionary diễn đạt lại. `example.en` = câu đặt trong ngữ cảnh của sách. Không thêm nghĩa, collocation, ghi chú nào ngoài unit.
- Tách được/không tách được, có tân ngữ hay không: đọc từ dạng trong Mini dictionary (`knock down sth or knock sth down`, `look after sb`, `come up`).
- Chỉ viết "sách ghi…/theo sách…" khi câu đó có thật trong src. Điều gì không chắc → **kiểm lại sách**, không đoán; vẫn không chắc → ghi vào *Todo for human*.
- Lỗi OCR: tin ảnh trang, không tin text OCR.
- **Kiểm trôi (drift audit) mỗi 5 unit**: chọn ngẫu nhiên 2 unit đã làm (kể cả lượt trước), đối chiếu lại từng thẻ với src/ảnh trang; ghi kết quả vào implementation-notes.
- Không sửa `tools/books.json`, GUID, note type, tên deck trừ khi tôi yêu cầu.

## 6. Tiếng Việt
Đúng nghĩa trước, rồi ngắn gọn, tự nhiên, dễ hiểu. Không dịch từng chữ gượng; không diễn giải đổi nghĩa. Dùng đúng bảng thuật ngữ trong STYLE_GUIDE §4 (tiểu từ, ngoại/nội động từ, tách được, tân ngữ, trang trọng/thân mật…).

## 7. Trước khi giao deck cuối cùng (khi làm xong tất cả)
1. `python3 epv.py check $(ls units | sed 's/.json//')` → 0 LỖI; rà mọi cảnh báo còn lại.
2. Kiểm trôi toàn bộ: mỗi unit mở lại src/ảnh trang, so headword + định nghĩa + ví dụ + lý thuyết. Sửa theo sách.
3. Rà tiếng Việt toàn bộ (đặc biệt đồng nghĩa/trái nghĩa – chỗ dễ sai nghĩa nhất).
4. `python3 epv.py audio && python3 epv.py selftest && python3 epv.py build && python3 epv.py verify` → 0 bad renders, đúng cây deck, audio đủ 100%.
5. Báo cáo: đã kiểm gì, sửa gì, còn gì chưa chắc.

## 8. Báo cáo mỗi lượt
**Luôn đính kèm `implementation-notes.md` riêng** (cùng `.apkg` và kit) sau mỗi lượt.
Tiếng Việt, ngắn gọn: bảng unit | chủ đề | số thẻ | LỖI; kết quả verify; Deviations; việc cần tôi quyết.
