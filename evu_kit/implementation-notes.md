# implementation-notes – English Vocabulary in Use (evu_kit)

## Tiến độ
| Sách (key) | PDF | Unit | Trạng thái |
|---|---|---|---|
| Elementary (ele) | EVU Elementary 3rd ed. (text PDF, không có dấu cách giữa từ → dựng lại từ khoảng cách glyph) | 60 | **xong 60/60** |
| Pre-intermediate & Intermediate (pre) | EVU Pre-int & Int 4th ed. | 100 | đang làm |
| Upper-intermediate (upp) | EVU Upper-int 4th ed. + demo (unit 1–4, 80–82) | 101 | chưa |
| Advanced (adv) | EVU Advanced | – | chưa |
| Business Intermediate (bus) | Business Vocabulary in Use Int 3rd ed. | – | chưa |
| Grammar & Vocabulary for Advanced (gva) | Hewings & Haines | – | chưa |

| Lượt | Phạm vi | Kết quả đo |
|---|---|---|
| E1 | Elementary 1–60 | 60 unit, 1244 mục; build 1305 note / 2549 thẻ (60 note lý thuyết + 1 mục lục); 0 bad renders; audio 1244/1244; GUID trùng 0; note logic trùng 0 |

## Quyết định thiết kế (đã đối chiếu 2 deck demo)
- **Note type & giao diện**: lấy nguyên từ demo `English Vocabulary In Use (Upper-Intermediate).apkg` – "(Vocab In Use) Nhìn từ đoán nghĩa" (13 field: Từ vựng, Định nghĩa (a), IPA, Định nghĩa (v), Dịch nghĩa, Câu ví dụ hoàn chỉnh, Dịch câu ví dụ, Trái nghĩa, Đồng nghĩa, Ngữ pháp, Phát âm, STT, Nguồn; 2 thẻ) + "Tóm tắt" (lý thuyết). Không thêm field (khác EPV: demo EVU không có field lý thuyết trong note từ vựng).
- **Cây deck** như demo: `<Root>::{Lý thuyết, Từ vựng (nhìn từ, đoán nghĩa), Từ vựng (nghe, gõ từ đúng)}::NN-Section::NN-Unit`, `01-Contents` = mục lục song ngữ, section đánh số từ 02 theo trang Contents của sách (khớp demo: upp `02-Effective vocabulary learning`, `08-Words and pronunciation`). Thẻ 1 → nhìn từ, thẻ 2 → nghe. Mỗi sách 1 file .apkg (giống demo; tránh file >100 MB).
- **Root** theo tên demo: `English Vocabulary In Use (Elementary)`, `(Pre-Intermediate and Intermediate)`, `(Upper-Intermediate)`, … Hai sách không mang tên EVU (Business Vocabulary in Use, Grammar and Vocabulary for Advanced) dùng đúng tên sách.
- **Câu ví dụ = nguyên văn câu sách** (demo dùng nguyên câu sách). `tools/compile.py` tự tìm câu chứa headword trên trang lý thuyết (ưu tiên chỗ in đậm), rồi trang bài tập; bôi đậm headword (kể cả dạng chia: bất quy tắc, -e/-y/gấp đôi phụ âm, rút gọn ’ve/’m/’s, phrasal verb tách được).
  - `exb=` : câu sách ghép lại bằng tay khi PDF trích rời (bảng 2–3 cột, bong bóng thoại) – vẫn là chữ của sách.
  - `ex=` : câu kit tự đặt khi từ chỉ có ở nhãn tranh/danh sách (demo cũng tự đặt câu cho mục lục). Tag `EVU::ex_kit`. Elementary: 425/1244 câu kit đặt (chủ yếu unit tranh: bộ phận cơ thể, quần áo, đồ bếp, quốc tịch…).
- **Mật độ thẻ**: mục in đậm trên trang lý thuyết + cụm thiết yếu ở mục Expressions/Common mistakes; không làm thẻ cho chữ thường không in đậm, không làm lại thẻ đã có ở unit trước của cùng sách (trừ nghĩa khác → `sense`). Trung bình Elementary 20,7 mục/unit (demo 40–70/unit có cả từ phổ thông không in đậm – bỏ để tránh thẻ ít giá trị theo yêu cầu "no redundant/low-value cards").
- **Lý thuyết**: tóm tắt song ngữ theo mục A/B/C… của trang (như EPV), không chép nguyên trang như demo – giữ nguyên tắc của dự án EPV (không chép đoạn dài), câu sách vẫn có trong thẻ.
- **IPA**: chuẩn Anh, viết tay (không dùng IPA máy). Demo upp dùng IPA Mỹ → build đổi sang chuẩn Anh bằng `uk_ipa` (như EPV).
- **Audio**: Kokoro TTS offline, giọng `bm_george` (như EPV), mp3 mono 24 kHz **64 kbps** (EPV 96 kbps) để apkg mỗi sách < 100 MB. `media/` không commit (tái tạo xác định bằng `evu.py audio`).
- **GUID**: `evu|book|unit|word|sense` (sha1) → build lại nhiều lần không nhân đôi; verify đếm GUID trùng + note logic trùng.
- **Nguồn PDF**: `tools/extract_src.py` dựng dòng từ glyph (rawdict): chèn dấu cách theo khoảng trống glyph (PDF Elementary không có ký tự cách), đánh dấu **in đậm**, sửa glyph ghép bị mất (fi/fl/ff…) bằng tần suất từ `wordfreq`, ghi mọi chỗ sửa ở dòng `### LIGATURE`.

## Deviations
- Elementary: `music` (u15 môn học / u26 sense general), `musical` (u24 phim / u26 sense adjective), `take off` (u4 cởi / u32 sense plane), `turn down` (u46 volume / refuse), `call` (u2 đặt tên / u17 sense phone), `hot`/`cold` (u7 cảm giác / u28 sense weather), `dry` (u11 lau khô / u28 sense weather), `back` (u3 lưng / u53 sense place), `right` (u53 phải / u54 sense correct), `well` (u6 khỏe / u54 sense manner), `get` (u45 become / obtain), `take` (u43 time / u44 carry), `play` (u23 / u24 sense act), `mug` (u11 cốc / u34 sense attack), `side` (u3 / u53 position), `water` (u36 tưới / u55 drink), `crash` (u36 computer), `fly` (u18 / u49 pilot), `carry`, `pass`, `after`, `like`, `for`, `do`, `single`, `delete`, `hope` – mỗi cặp là nghĩa khác, có `sense`.
- Mục đã có thẻ ở unit trước không làm lại (chỉ nhắc trong lý thuyết): ví dụ u13 bỏ `turn off` (u12), u40 bỏ `do nothing` (u25) và `What do you do?` (u14), u47 hầu hết việc hằng ngày đã có ở u12/u13/u38/u41.
- Câu sách có lỗi in (`nationalies` u27) giữ nguyên trong src; ví dụ dùng câu đã ghép tay (`exb`).

## Kiểm trôi
- E1: mọi unit chạy `compile` có in ngữ cảnh câu được chọn; soát từng câu với bản dịch, sửa các trường hợp câu tự động chọn khác câu đã dịch (u5 old/fair, u8 bảng ngày lễ, u9 bảng từ, u10 fruit/vegetables, u12 shower, u18 danh sách đồ mang theo, u23 tennis/badminton/swimming, u26 music/musical/musician/band, u32 arrive/check, u34 robbery/mugging, u38 have to/had to/have got, u39 go…, u58 bảng tiền tố). Sau mỗi lần sửa bộ tách câu, compile lại toàn bộ và `git diff` units để chắc câu cũ không đổi ngoài ý muốn.

## Todo for human
- 425 câu ví dụ Elementary là câu kit đặt (tag `EVU::ex_kit`) vì từ chỉ xuất hiện ở nhãn tranh / bảng; lọc bằng tag nếu muốn xem lại.
- Lý thuyết là bản tóm tắt song ngữ, không chép nguyên trang như demo – nếu muốn chép nguyên trang như demo, cần quyết định riêng (vấn đề bản quyền và độ dài).
