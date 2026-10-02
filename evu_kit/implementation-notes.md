# implementation-notes – English Vocabulary in Use (evu_kit)

## Tiến độ
| Sách (key) | PDF | Unit | Trạng thái |
|---|---|---|---|
| Elementary (ele) | EVU Elementary 3rd ed. (text PDF, không có dấu cách giữa từ → dựng lại từ khoảng cách glyph) | 60 | **xong 60/60** |
| Pre-intermediate & Intermediate (pre) | EVU Pre-int & Int 4th ed. | 100 | **xong 100/100** |
| Upper-intermediate (upp) | EVU Upper-int 4th ed. + demo (unit 1–4, 80–82) | 101 | **xong 94 unit mới + 7 unit demo giữ nguyên** |
| Advanced (adv) | EVU Advanced 3rd ed. | 101 | **xong 101/101** |
| Business Intermediate (bus) | Business Vocabulary in Use Int 3rd ed. | 66 | **xong 66/66** |
| Grammar & Vocabulary for Advanced (gva) | Hewings & Haines | 45 | **xong 45/45** |

| Lượt | Phạm vi | Kết quả đo |
|---|---|---|
| E1 | Elementary 1–60 | 60 unit, 1244 mục; build 1305 note / 2549 thẻ (60 note lý thuyết + 1 mục lục); 0 bad renders; audio 1244/1244; GUID trùng 0; note logic trùng 0 |
| E2 | Pre-int & Int 1–100 | 100 unit, 2260 mục (365 câu kit đặt); build 2361 note / 4621 thẻ (100 note lý thuyết + 1 mục lục); 0 bad renders; audio 2260/2260; GUID trùng 0; note logic trùng 0 |
| E3 | Upper-int 5–79, 83–101 (+ demo 1–4, 80–82) | 94 unit, 2486 mục mới (784 câu kit đặt); build 3124 note / 6146 thẻ (2486 mới + 94 lý thuyết + 544 note demo giữ nguyên, 291 IPA demo đổi sang chuẩn Anh); 0 bad renders; audio 3022/3022; GUID trùng 0; note logic trùng 0 |
| E4 | Advanced 1–101 | 101 unit, 2654 mục (347 câu kit đặt); build 2756 note / 5410 thẻ (101 note lý thuyết + 1 mục lục); 0 bad renders; audio 2654/2654; GUID trùng 0; note logic trùng 0 |
| E6 | GVA 1–45 | 45 unit, 1083 mục (129 câu kit đặt); build 1129 note / 2212 thẻ (45 note lý thuyết + 1 mục lục); 0 bad renders; audio 1083/1083; GUID trùng 0; note logic trùng 0 |
| E5 | Business Int 1–66 | 66 unit, 1220 mục (45 câu kit đặt); build 1287 note / 2507 thẻ (66 note lý thuyết + 1 mục lục); 0 bad renders; audio 1220/1220; GUID trùng 0; note logic trùng 0 |

## Quyết định thiết kế (đã đối chiếu 2 deck demo)
- **Note type & giao diện**: lấy nguyên từ demo `English Vocabulary In Use (Upper-Intermediate).apkg` – "(Vocab In Use) Nhìn từ đoán nghĩa" (13 field: Từ vựng, Định nghĩa (a), IPA, Định nghĩa (v), Dịch nghĩa, Câu ví dụ hoàn chỉnh, Dịch câu ví dụ, Trái nghĩa, Đồng nghĩa, Ngữ pháp, Phát âm, STT, Nguồn; 2 thẻ) + "Tóm tắt" (lý thuyết). Không thêm field (khác EPV: demo EVU không có field lý thuyết trong note từ vựng).
- **Cây deck** như demo: `<Root>::{Lý thuyết, Từ vựng (nhìn từ, đoán nghĩa), Từ vựng (nghe, gõ từ đúng)}::NN-Section::NN-Unit`, `01-Contents` = mục lục song ngữ, section đánh số từ 02 theo trang Contents của sách (khớp demo: upp `02-Effective vocabulary learning`, `08-Words and pronunciation`). Thẻ 1 → nhìn từ, thẻ 2 → nghe. Mỗi sách 1 file .apkg (giống demo; tránh file >100 MB).
- **Root** theo tên demo: `English Vocabulary In Use (Elementary)`, `(Pre-Intermediate and Intermediate)`, `(Upper-Intermediate)`, … Hai sách không mang tên EVU (Business Vocabulary in Use, Grammar and Vocabulary for Advanced) dùng đúng tên sách.
- **Câu ví dụ = nguyên văn câu sách** (demo dùng nguyên câu sách). `tools/compile.py` tự tìm câu chứa headword trên trang lý thuyết (ưu tiên chỗ in đậm), rồi trang bài tập; bôi đậm headword (kể cả dạng chia: bất quy tắc, -e/-y/gấp đôi phụ âm, rút gọn ’ve/’m/’s, phrasal verb tách được).
  - `exb=` : câu sách ghép lại bằng tay khi PDF trích rời (bảng 2–3 cột, bong bóng thoại) – vẫn là chữ của sách.
  - `ex=` : câu kit tự đặt khi từ chỉ có ở nhãn tranh/danh sách (demo cũng tự đặt câu cho mục lục). Tag `EVU::ex_kit`. Elementary: 357/1244 câu kit đặt (chủ yếu unit tranh: bộ phận cơ thể, quần áo, đồ bếp, quốc tịch…).
- **Mật độ thẻ**: mục in đậm trên trang lý thuyết + cụm thiết yếu ở mục Expressions/Common mistakes; không làm thẻ cho chữ thường không in đậm, không làm lại thẻ đã có ở unit trước của cùng sách (trừ nghĩa khác → `sense`). Trung bình Elementary 20,7 mục/unit (demo 40–70/unit có cả từ phổ thông không in đậm – bỏ để tránh thẻ ít giá trị theo yêu cầu "no redundant/low-value cards").
- **Lý thuyết**: tóm tắt song ngữ theo mục A/B/C… của trang (như EPV), không chép nguyên trang như demo – giữ nguyên tắc của dự án EPV (không chép đoạn dài), câu sách vẫn có trong thẻ.
- **IPA**: chuẩn Anh, viết tay (không dùng IPA máy). Demo upp dùng IPA Mỹ → build đổi sang chuẩn Anh bằng `uk_ipa` (như EPV).
- **Audio**: Kokoro TTS offline, giọng `bm_george` (như EPV), mp3 mono 24 kHz **64 kbps** (EPV 96 kbps) để apkg mỗi sách < 100 MB. `media/` không commit (tái tạo xác định bằng `evu.py audio`).
- **GUID**: `evu|book|unit|word|sense` (sha1) → build lại nhiều lần không nhân đôi; verify đếm GUID trùng + note logic trùng.
- **Nguồn PDF**: `tools/extract_src.py` dựng dòng từ glyph (rawdict): chèn dấu cách theo khoảng trống glyph (PDF Elementary không có ký tự cách), đánh dấu **in đậm**, sửa glyph ghép bị mất (fi/fl/ff…) bằng tần suất từ `wordfreq`, ghi mọi chỗ sửa ở dòng `### LIGATURE`.

## Deviations
- Elementary: `music` (u15 môn học / u26 sense general), `musical` (u24 phim / u26 sense adjective), `take off` (u4 cởi / u32 sense plane), `turn down` (u46 volume / refuse), `call` (u2 đặt tên / u17 sense phone), `hot`/`cold` (u7 cảm giác / u28 sense weather), `dry` (u11 lau khô / u28 sense weather), `back` (u3 lưng / u53 sense place), `right` (u53 phải / u54 sense correct), `well` (u6 khỏe / u54 sense manner), `get` (u45 become / obtain), `take` (u43 time / u44 carry), `play` (u23 / u24 sense act), `mug` (u11 cốc / u34 sense attack), `side` (u3 / u53 position), `water` (u36 tưới / u55 drink), `crash` (u36 computer), `fly` (u18 / u49 pilot), `carry`, `pass`, `after`, `like`, `for`, `do`, `single`, `delete`, `hope` – mỗi cặp là nghĩa khác, có `sense`.
- Mục đã có thẻ ở unit trước không làm lại (chỉ nhắc trong lý thuyết): ví dụ u13 bỏ `turn off` (u12), u40 bỏ `do nothing` (u25) và `What do you do?` (u14), u47 hầu hết việc hằng ngày đã có ở u12/u13/u38/u41.
- Pre-int: unit 30 (biển báo dạng ảnh) – chữ trên biển đọc từ ảnh trang PDF (render), ví dụ = chữ biển + chú thích của sách. Các unit ôn (66–100: chức năng giao tiếp, cụm cố định, phrasal verb, tiền/hậu tố) bỏ mục đã có thẻ ở unit trước; nghĩa khác đặt `sense` (vd `take` time/accept, `run` manage/computer/transport, `miss` transport/person, `point` decimal/opinion).
- `exb` đôi khi đổi chủ ngữ đại từ thành danh từ hoặc lược mệnh đề phụ để câu đứng độc lập (vd *Harry’s girlfriend was getting jealous* thay *his girlfriend…*) – vẫn là chữ của sách.
- `evu.py`: sửa đọc số unit từ tên tệp (hỗ trợ unit 100) và kiểm trùng theo unit nhỏ nhất.
- Upper-int: kiểm trùng gồm cả từ của 7 unit demo (`tools/upp_demo_words.json`, trích từ apkg demo) → bỏ từ demo đã có (vd `luggage`, `rectangle`, `knowledge`, `progress`, `weather`, `pair`, `roar`, `crash`), nghĩa khác đặt `sense` (vd `make up` invent ≠ demo constitute, `object` protest). Unit 99 (biển báo) và 100C (tiêu đề chơi chữ) đọc chữ từ ảnh trang PDF. Unit ngữ pháp từ vựng (70–78, 83–88, 100–101) phần lớn là danh sách không có câu → câu kit đặt nhiều (u70 47, u71 56, u75 43, u101 36). Trường `Ngữ pháp` không để trống: thêm `tools/fixg.py` điền ghi chú khi check báo thiếu.
- Advanced: kiểm trùng toàn sách trước khi viết (grep headword) → từ đã có ở unit trước bị bỏ (vd `truce`, `ceasefire`, `standing ovation`, `remorse`, `yearn`, `webinar`, `breathalyser`, `e-commerce`, `overrated`, `condolences`, `contaminate`, `reach a compromise`, `a dog’s life`, `the deceased`); nghĩa khác đặt `sense` (vd `mourn` tiếc nuối ≠ `mourning` để tang, `conceive` nghĩ ra ≠ có thai, `comprehensive` toàn diện ≠ trường phổ thông, `besieged` bị nhà báo vây ≠ `besiege` quân sự, `crawl` nịnh ≠ bò). Unit 91 (đa nghĩa: fair/flat/capital/mean) tách mỗi nghĩa 1 note có `sense`. `tools/mk.sh` gộp fixg `--auto` + make, chỉ in LỖI/trùng.
- Business: trang trái = lý thuyết (index 9+2u). Sách song song nhiều cụm hội thoại (gọi điện, họp, thuyết trình, đàm phán) → thẻ là cụm cố định (pos `cl`/`excl`) với câu sách. Kiểm trùng toàn sách (vd `overtime`, `CAD/CAM`, `outsource`, `raw materials`, `loss-leader`, `make a profit`, `financial year`, `put off/back`, `eye contact` chỉ thẻ ở unit đầu). Unit 24 đọc sơ đồ phân phối từ ảnh trang. Nhãn dụng cụ thuyết trình (u60) đổi sang câu kit vì sách chỉ có nhãn ảnh.
- GVA: sách là OCR (KEY rỗng). Unit 1–25 ngữ pháp → thẻ pos `st` (cấu trúc), headword = tên/khung cấu trúc, ví dụ = câu sách với cấu trúc trong `[ ]`, mục lý thuyết theo `## 2.N` của sách. Unit 26–45 từ vựng → thẻ từ các bài đọc, Vocabulary note, bài ghép định nghĩa; ô trống bài tập chỉ điền khi đáp án hiển nhiên từ hộp từ/ngữ cảnh; câu đã viết lại (thay từ đồng nghĩa, điền chỗ trống không chắc) đánh dấu `ex=` (kit) chứ không `exb=`. Bỏ các thẻ chỉ dựa trên phần nghe (không có script). Sửa lỗi OCR trong câu sách (vd `there would be`, `The cloud's building up`).
- Câu sách có lỗi in (`nationalies` u27) giữ nguyên trong src; ví dụ dùng câu đã ghép tay (`exb`).

## Kiểm trôi
- E1: mọi unit chạy `compile` có in ngữ cảnh câu được chọn; soát từng câu với bản dịch, sửa các trường hợp câu tự động chọn khác câu đã dịch (u5 old/fair, u8 bảng ngày lễ, u9 bảng từ, u10 fruit/vegetables, u12 shower, u18 danh sách đồ mang theo, u23 tennis/badminton/swimming, u26 music/musical/musician/band, u32 arrive/check, u34 robbery/mugging, u38 have to/had to/have got, u39 go…, u58 bảng tiền tố). Sau mỗi lần sửa bộ tách câu, compile lại toàn bộ và `git diff` units để chắc câu cũ không đổi ngoài ý muốn.

## Todo for human
- Upper-int: 784/2486 câu ví dụ do kit đặt (tag `EVU::ex_kit`), tập trung ở unit danh sách (hậu tố/tiền tố, danh từ ghép, viết tắt, US English, từ báo chí). 1758 mục có ghi chú `Ngữ pháp` ngắn (<15 từ, cảnh báo mềm của check; pre 1144).
- Advanced: 347/2654 câu ví dụ do kit đặt (tag `EVU::ex_kit`), tập trung ở unit danh sách không có câu (u65 màu sắc 29, u79 từ học thuật 29, u85 viết tắt 26, u69 khó khăn 23, u86 tiền tố 17). 1547 cảnh báo mềm `Ngữ pháp` ngắn.
- Business: 45/1220 câu ví dụ do kit đặt; 692 cảnh báo mềm `Ngữ pháp` ngắn.
- GVA: 129/1083 câu ví dụ do kit đặt (chủ yếu danh sách cụm từ/ảnh không có câu); cảnh báo mềm `Ngữ pháp` ngắn.
- Pre-int: 365/2260 câu ví dụ do kit đặt (tag `EVU::ex_kit`), chủ yếu unit tranh (thức ăn, động vật, cơ thể, quần áo, đồ văn phòng).
- 357 câu ví dụ Elementary là câu kit đặt (tag `EVU::ex_kit`) vì từ chỉ xuất hiện ở nhãn tranh / bảng; lọc bằng tag nếu muốn xem lại.
- Lý thuyết là bản tóm tắt song ngữ, không chép nguyên trang như demo – nếu muốn chép nguyên trang như demo, cần quyết định riêng (vấn đề bản quyền và độ dài).
