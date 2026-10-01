# implementation-notes – English Phrasal Verbs in Use

## Tiến độ
| Sách | Có sẵn | Còn làm |
|---|---|---|
| Advanced (60) | unit 1–15 (demo) + *New phrasal verbs* (bản 1) + **16–20** (lượt 1) + **21–25** (lượt 2) + **26–30** (lượt 3) + **31–35** (lượt 4) + **36–40** (lượt 5) + **41–45** (lượt 6) + **46–50** (lượt 7) + **51–55** (lượt 8) + **56–60** (lượt 9) + **bổ sung 1–15** (lượt 10) | – (xong) |
| Intermediate (70) | – | 1–70 |

| Lượt | Unit | Số thẻ | Ghi chú |
|---|---|---|---|
| 0 | kit | – | tạo kit, kiểm chứng kit với sách (bên dưới) |
| 1 | Adv 16–20 | 81 mục / 162 thẻ + 5 note lý thuyết | bản 1a (tóm tắt tự do) bị bạn bác vì có ý ngoài sách → **1b: làm lại toàn bộ theo chế độ bám sách – diễn giải** (STYLE_GUIDE §0); build 450 note / 878 thẻ, 0 bad renders |
| 2 | Adv 21–25 | 90 mục / 180 thẻ + 5 note lý thuyết + 90 audio | chế độ bám sách – diễn giải; build 545 note / 1063 thẻ, 0 bad renders, audio 171/171 |
| 3 | Adv 26–30 | 92 mục / 184 thẻ + 5 note lý thuyết + 92 audio | build 642 note / 1252 thẻ, 0 bad renders, audio 263/263 |
| 4 | Adv 31–35 | 93 mục / 186 thẻ + 5 note lý thuyết + 93 audio | build 740 note / 1443 thẻ, 0 bad renders, audio 356/356 |
| 5 | Adv 36–40 | 86 mục / 172 thẻ + 5 note lý thuyết + 86 audio | build 831 note / 1620 thẻ, 0 bad renders, audio 442/442 |
| 6 | Adv 41–45 | 92 mục / 184 thẻ + 5 note lý thuyết + 92 audio | build 928 note / 1809 thẻ, 0 bad renders, audio 534/534 |
| 7 | Adv 46–50 | 96 mục / 192 thẻ + 5 note lý thuyết + 96 audio | build 1029 note / 2006 thẻ, 0 bad renders, audio 630/630 |
| 8 | Adv 51–55 | 92 mục / 184 thẻ + 5 note lý thuyết + 92 audio | build 1126 note / 2195 thẻ, 0 bad renders, audio 722/722 |
| 9 | Adv 56–60 | 66 mục / 132 thẻ + 5 note lý thuyết + 66 audio | build 1197 note / 2332 thẻ, 0 bad renders, audio 788/788 |
| 10 | Adv bổ sung 1–15 | 44 mục / 88 thẻ + 44 audio (dùng lý thuyết demo) | build 1241 note / 2420 thẻ, 0 bad renders, audio 832/832 |
| 11 | Int 1–10 | 177 mục / 354 thẻ + 10 note lý thuyết (+ Contents) + 177 audio | build 1429 note / 2785 thẻ, 0 bad renders, audio 1009/1009 |
| 12 | Int 11–15 | 77 mục / 154 thẻ + 5 note lý thuyết + 77 audio | build 1511 note / 2944 thẻ, 0 bad renders, audio 1086/1086 |
| 13 | Int 16–20 | 81 mục / 162 thẻ + 5 note lý thuyết + 81 audio | build 1597 note / 3111 thẻ, 0 bad renders, audio 1167/1167 |
| 14 | Int 21–25 | 70 mục / 140 thẻ + 5 note lý thuyết + 70 audio | build 1672 note / 3256 thẻ, 0 bad renders, audio 1237/1237 |
| 15 | Int 26–30 | 61 mục / 122 thẻ + 5 note lý thuyết + 61 audio | build 1738 note / 3383 thẻ, 0 bad renders, audio 1298/1298 |

## Quyết định (xem PROMPT.md §3)
D1 thứ tự Adv 16→60 → bổ sung demo → Int 1→70 · D2 IPA chuẩn Anh (config.ipa_style) · D3 1 deck gốc `English Phrasal Verbs in Use` → `Advanced`/`Intermediate` · D4 thẻ demo chỉ có ở bản 1: giữ + tag `EPV::demo_ban1` · D5 audio **bắt buộc**: Kokoro TTS offline, giọng Anh–Anh nam `bm_george` (sửa từ lượt 1c; trước đó để trống) · D6 chọn mục theo Mini dictionary + cụm in đậm.

## Kiểm chứng kit với sách (lượt 0)
- **Ấn bản**: cả 2 PDF là 2nd edition (trang Acknowledgements Advanced ghi Unit 23 *Agreeing* và Unit 33 *Lectures and seminars* là bài mới của bản 2; PDF Intermediate có tiêu đề "CAM ENG Phrasal Verbs Intermediate 2nd edition").
- **Tên unit / phân mục** (`tools/books.json`): Advanced 60/60 tiêu đề khớp chữ trên trang lý thuyết (tự động, `epv.py selftest`). Intermediate 70/70: 66 khớp OCR; unit 2, 4, 20, 33, 44, 48, 54, 58, 63, 64 kiểm lại bằng OCR phần đầu trang độ phân giải cao; unit 62 *Travel* đầu trang chỉ in mục "Going on a journey" – xác nhận qua mục lục (trang 128 = trang của unit 62). Phân mục lấy từ mục lục; nhóm 42–50 là *Work, study and finance*.
- **Công thức trang** kiểm bằng khớp tiêu đề cho cả 130 unit.
- **Demo ↔ bản 2**: so từ nội dung lý thuyết demo với trang sách: demo 1–8 → bản 2 unit 1–8 (68–88%); demo 10–16 → bản 2 unit 9–15 (69–81%); mọi unit khác ≤ 27%. Demo 9 *New phrasal verbs* không khớp unit nào (≤ 21%) → chỉ có ở bản 1.
- **Thẻ demo (320, không tính New phrasal verbs)**: 310 headword có trên trang sách bản 2; 3 sai dạng (`hit upon`, `bear upon`, `call upon` → sách: `hit on`, `bear on`, `call on`, đã sửa khi build); 4 chỉ có ở bản 1 (`flirt with somebody`, `flirt with something` – unit 5; `wake up and smell the coffee` – unit 8, bản 2 dạy *wake up to the fact*; `wake up` – unit 14) → tag `EPV::demo_ban1`; 3 còn lại khớp khi xét dạng chia (*gunning for*, *took it for a joyride*, *drop out*).
  Ví dụ demo: 168 câu của sách, 77 khớp một phần, 75 không lấy từ sách (demo tự viết) – chưa sửa, xem Todo.
- **Mini dictionary bản 2 so với thẻ demo** (ứng viên bổ sung, cần kiểm tay – so khớp tự động còn nhiễu):

| Unit | Thẻ demo | Mục Mini dict | Chưa có thẻ | Mục |
|---|---|---|---|---|
| 1 | 34 | 35 | 9 | breakaway; breakout; come along; lockout; send in sb or send sb in; shake-up; shutdown; wear out sb or wear sb out; work out sth or work sth out |
| 2 | 25 | 25 | 0 |  |
| 3 | 22 | 32 | 9 | buy out sb/sth or buy sb/sth out; downpour; lift-off; lookout; outbreak; outlook; output; stow away; walk out |
| 4 | 19 | 24 | 6 | fallback; left out; outgoing; outspoken; outstretched; worked up |
| 5 | 14 | 12 | 2 | be riddled with sth; stream into swh |
| 6 | 16 | 40 | 27 | ask out sb or ask sb out; back up (sth) or back (sth) up; bail out sb/sth or bail sb/sth out; base sth on sth; be asking for sth; be gunning for sb; buy up sth or buy sth up; carry forward sth or carry sth forward; fall through; get by; gloss over sth; go into sth; go over to sth; hack into sth; hang about/around/round with sb; log in/into sth; look after sb/sth; predispose sb to/towards sth; print off sth or print sth off; put out sth or put sth out; scroll down/up; sell up (sth) or sell (sth) up; square up; sum up (sth/sb) or sum (sth/sb) up; take on sth or take sth on; take over sth or take sth over; turn over sth or turn sth over |
| 7 | 25 | 26 | 4 | climb down; nose about/around (swh); warm up sb or warm sb up; warm up sth or warm sth up |
| 8 | 21 | 19 | 2 | be going round in circles; come into one’s own |
| 9 | 15 | 22 | 7 | blunder about/around; crowd around/round (sth/sb); knock sb about/around; knock sth about/around; roll about/around; turn around/round (sb/sth) or turn (sth/sb) around/round; turn around/round sth or turn sth around |
| 10 | 20 | 20 | 2 | take down sth or take sth down; water down sth or water sth down |
| 11 | 17 | 15 | 0 |  |
| 12 | 21 | 19 | 0 |  |
| 13 | 27 | 20 | 0 |  |
| 14 | 23 | 19 | 3 | cry out (sth) or cry (sth) out; scream out (sth) or scream (sth) out; shout out (sth) or shout (sth) out |
| 15 | 21 | 21 | 1 | prop yourself up |

- **Chuẩn hoá demo khi build** (kiểm trong gói .apkg sau build): nhãn từ loại (`noun`→`n.`, `adjective`→`adj.`); IPA Mỹ → Anh theo luật (oʊ→əʊ, ɛ→e, ɑ→ɒ, ɑr→ɑː, ɔ→ɒ trước f/s/ŋ/g/θ và ɔː ở chỗ khác, bỏ r sau nguyên âm; từ nhóm *ask/after/branch…* æ→ɑː) – 0 thẻ còn ký hiệu Mỹ; STT và tiêu đề "Unit N/Bài N" đổi số theo bản 2; bài bản 1 *New phrasal verbs* có STT `B1-09` và tiêu đề "Unit 9 (bản 1)" để không trùng unit 9 bản 2; mục lục (00-Contents) thay bằng mục lục bản 2 (có unit 16 *Time*, 23 *Agreeing*, 33 *Lectures and seminars*, không có *New phrasal verbs*).
- **Lỗi tìm thấy ở lượt kiểm cuối và đã sửa**: STT 009 trùng (42 thẻ) → tách `B1-09`; tag bản 1 thiếu `wake up` (ghi nhầm số unit bản 2); IPA còn `ɔ`/`æ` kiểu Mỹ → thêm luật.
- **Nguồn src/**: Advanced trích bằng pymupdf (có danh sách in đậm). Intermediate OCR tesseract 300 dpi – có lỗi chữ, trộn cột; **không** có in đậm → luôn xem ảnh trang.

## Final check deck lượt 0 (chỉ demo, chưa có unit mới)
- 364 note / 711 thẻ, 0 bad renders; cây deck: `English Phrasal Verbs in Use::Advanced::{Lý thuyết, Từ vựng (nhìn từ, gõ nghĩa), Từ vựng (nghe, gõ từ đúng)}::<phân mục>::<unit>`; 347/347 thẻ demo giữ audio, 324 file media.

## Deviations
**Lượt 1 (Adv 16–20)**
- **Chế độ bám sách – diễn giải** (người dùng chốt ở lượt 1b): không chép nguyên văn nhưng mọi thông tin lấy từ unit; lý thuyết diễn giải từng mục của sách; ví dụ đặt trong ngữ cảnh sách. Bản 1a (tóm tắt tự do) có ý ngoài sách (*eke out a living*, *summon up courage*, nghĩa ‘chia tay’…) – đã xoá hết.
- `epv.py check` đổi: cảnh báo ví dụ trùng sách ≥ 60%, def_en ≥ 70%, lý thuyết ≥ 12 từ liên tiếp; **mới**: collocation trong grammar_vi phải có trong src unit; in tỉ lệ đồng/trái nghĩa không có trong src (lượt 1b: 3/191).
- Ví dụ: đã rà tay các câu bài tập có chỗ trống (check không bắt được) và viết lại ~40 câu quá sát câu sách.
- Sửa lỗi `check`: `vi_issues` gỡ thẻ HTML trước khi bỏ `<i>/<b>`, nên luôn báo nhầm "còn từ tiếng Anh" ở mọi ví dụ in nghiêng.
- Thêm helper `SEP/INS/INT/G/NOTE/REG` vào `tools/common.py`.
- Không làm thẻ vì demo đã có **cùng nghĩa**: `associate sth with sth` (u18 ↔ demo u2), `open up`, `press on` (u19 ↔ demo u15, u13), `set on`, `strike back` (u20 ↔ demo u3, u1).
- Làm thẻ dù trùng chữ với demo vì **khác nghĩa** (có `sense`): `fit in` (time; demo u11 = hòa nhập), `add up` (make sense; demo u1 = cộng), `depend on` (be influenced by; demo u13).
- `bump off` (u20) trùng 3 thẻ demo bài bản 1 *New phrasal verbs* – giữ vì bản 2 dạy ở u20.
- `break up` có 3 nghĩa ở 3 unit: `period of time` (u16), `meeting` (u19), `fight` (u20).
- `fit in`, `hurry along` (u16): Mini dictionary ghi dạng không tân ngữ nhưng trang sách dùng có tân ngữ, tách được (*fit revision in*, *hurrying those sales reports along*) → grammar_vi theo cách dùng trên trang.
- `add up` (u17): Mini dictionary không có nhãn, nhưng chú thích trên trang ghi *slightly informal* → register `informal`. `attribute`, `impact on`: *slightly formal* → `formal`.
- Cảnh báo coverage còn lại là báo nhầm của heuristic: `point to/towards` (đã có thẻ `point to something`), `push sb about/around/round` (đã có `push somebody around`).

**Lượt 1c (audio)**
- Thêm audio cho 81 thẻ Adv 16–20 (field *Phát âm*, đọc headword). Kokoro TTS offline (`kokoro-onnx`, model từ GitHub release), giọng Anh–Anh **nam** `bm_george` – demo dùng giọng nam (cao độ đo ~120 Hz), mp3 mono 24 kHz 96 kbps như demo.
- Soát phoneme TTS với IPA thẻ: 3 chỗ đọc sai đã sửa bằng `tts_phonemes` – *impact on* và *attribute … to* (TTS đọc trọng âm danh từ), *pass somebody by* (TTS đọc /æ/ thay vì /ɑː/).
- `build` báo LỖI nếu mục nào thiếu audio; `verify` in `audio thẻ mới: 81/81 – đủ`.
- Chỉ đọc headword (giống demo), không đọc câu ví dụ.

**Lượt 2 (Adv 21–25)**
- Không làm lại vì demo/lượt trước đã có **cùng nghĩa**: `drone on` (u21 ↔ demo u13), `count out` (u23 ↔ demo u14), `prop up` (u25 ↔ demo, nghĩa ‘chống, kê cho đứng’). Mục Mini dictionary ghi cho 2 unit (`cave in`, `defer to`, `go with` – u22 & u23; `space out` – u16 & u25): làm thẻ ở unit đầu tiên, unit sau chỉ nhắc trong lý thuyết.
- Làm thẻ dù trùng chữ vì **khác nghĩa** (có `sense`): `break down` (u24 ‘chia nhỏ’; demo u4 ‘hỏng’), `pick up` (u24 ‘tiếp thu thông tin’; demo có nhiều nghĩa khác – nghĩa ‘learn a skill/language’ ở demo u1 gần nhất, xem Todo), `keep up` (u24 ‘theo kịp’), `come at something` (u24 ‘tiếp cận vấn đề’; u20 là `come at somebody` ‘lao vào’).
- Thêm mục in đậm không có trong Mini dictionary nhưng được dạy trên trang: `back down` (u23).
- `come to (an agreement)` (u23): làm thẻ dạng `come to an agreement` (pos `phrase`) để audio đọc đủ cụm.
- Sửa phát âm TTS bằng `tts_phonemes`: *blast* (BATH /ɑː/), *bow to* (/baʊ/, TTS đọc /bəʊ/), *separate off/out* (động từ /ˈsepəreɪt/, TTS đọc kiểu tính từ).
- `check`: bỏ báo nhầm "grammar_vi nói 'sách…'" khi chữ *sách* nằm trong *chính sách, ngân sách, danh sách, giá sách, sách đọc*.

**Lượt 3 (Adv 26–30)**
- Không làm lại vì demo/lượt trước đã có **cùng nghĩa**: `sail through` (u27 ↔ demo u5), `get by` (u27 ↔ demo u1, ‘xoay xở vừa đủ’), `smooth over` (u28 ↔ u23), `come round to` / `come around` (u29 ↔ u23 – thẻ u23 đã ghi cách dùng không tân ngữ `come round`), `tie somebody down` (u29 ↔ demo u11).
- Làm thẻ dù trùng chữ vì **khác nghĩa** (có `sense`): `add up` (u26 ‘cộng dồn thành khoản lớn’), `build up`, `knock down` (u26 ‘hạ giá’; demo ‘phá đổ’, ‘xô ngã’), `round up` (u26 ‘làm tròn số’; u25 ‘gom người’), `put on` (u26 ‘tăng cân’), `push up`, `fall off`, `come out` (u27), `get through` (u27 ‘qua kỳ thi’), `break down` (u28 ‘quan hệ đổ vỡ’), `clear up`, `run into` (u28), `push through`, `work out` (u29), `Come on!`, `Go on!`, `go ahead`, `Hang on!` (‘khoan đã’; demo `hang on` ‘phụ thuộc’), `Wake up!` (‘chú ý vào’; demo ‘thức dậy’).
- u29: thêm `do in`, `do yourself up`, `do without` (Mini dictionary + Tip của sách); `do out` (trang trí) chỉ có trong Tip, không có trong Mini dictionary → chỉ nhắc trong lý thuyết.
- u30 (câu cảm thán): headword giữ dấu `!` như Mini dictionary; `Shut up!` + `shut (sb) up` gộp một thẻ `shut up`; `Hang about/on!` → thẻ `Hang on!` (ghi chú *Hang about!*). Register: `Grow up!`, `Shut up!` = very informal (sách đánh dấu * vì dễ xúc phạm). Mục A của u30 là tranh minh họa → bối cảnh lấy từ tranh (đã xem ảnh trang).
- Sửa phát âm TTS: *live with* (TTS đọc /laɪv/ → /lɪv/), *grasp at* (BATH /ɑː/), *Roll on …!* (bỏ dấu …).

**Lượt 4 (Adv 31–35)**
- Không làm lại vì demo/lượt trước đã có **cùng nghĩa**: `drop out`, `mark down`, `move up`, `pore over`, `sail through` (u32 ↔ demo), `get through` (u32 ↔ u27), `round off` (u33 ↔ demo u13), `contend with` (u34 ↔ demo u2), `result in` (u34 ↔ u17).
- Làm thẻ dù trùng chữ vì **khác nghĩa** (có `sense`): `ease off` (u31 ‘làm việc nhẹ đi’; demo ‘dịu bớt’), `get off` (‘tan làm’), `pack in` (u31 ‘bỏ việc’; u27 ‘làm được nhiều việc’), `come across` (u32 ‘được truyền tải rõ’; demo ‘tình cờ gặp’), `fall behind` (u32 ‘không theo kịp’; u27 ‘kém điểm’), `finish off`, `get down` (u33; demo ‘làm kiệt sức’, ‘làm buồn’), `bring in` (u35 ‘thu hút khách’; demo ‘kiếm được tiền’), `look after` (u35 ‘lo mảng việc’; demo ‘chăm sóc’), `set up` (u35 ‘cấp vốn lập nghiệp’; demo ‘sắp xếp’), `break into`, `bring out`, `turn out`, `turn over` (u35).
- u32: `get in` và `get into` làm 2 thẻ (Mini dictionary tách 2 mục); `tick off` và `check off` cũng 2 thẻ.
- u34: mọi động từ đặt register `formal` (sách ghi cả bài hợp với bài luận trang trọng); động từ + giới từ dùng pos `v.`.
- Sửa phát âm TTS: *pass over*, *run around after*, *look after* (BATH /ɑː/), *object to* (động từ /əbˈdʒekt/, TTS đọc kiểu danh từ).

**Lượt 5 (Adv 36–40)**
- Không làm lại vì demo/lượt trước đã có **cùng nghĩa**: `clean out` (u36 ↔ demo u15 ‘lấy sạch’), `tie back` (u38 ↔ demo u2), `flirt with` (u39 ↔ demo u5), `pride yourself on` (u40 ↔ u27).
- Làm thẻ dù trùng chữ vì **khác nghĩa** (có `sense`): `break into` (u36 ‘động vào tiền để dành’), `come into` (‘thừa kế’), `run through` (‘tiêu sạch’), `set somebody back` (‘tốn tiền’), `square up`, `work off` (‘trả nợ’; demo ‘xả cảm xúc’), `clean up after` (u37), `have on` (u37 ‘đang bật’ / u38 ‘đang mặc’), `put up` (‘lắp kệ’), `put out`, `put away`, `pull up` (‘kéo ghế’), `get into` (u38 ‘mặc vừa’), `take up` (u38 ‘lên gấu’), `let down`, `let out`, `bust-up` (u39 ‘rạn nứt quan hệ’; u20 ‘trận cãi to’), `come out` (u39 ‘đi chơi’), `bring out` (u40 ‘khơi dậy phẩm chất’), `come across` (u40 ‘tỏ ra’), `draw out` (‘giúp tự tin’), `be getting on` (u40 ‘có tuổi’; u16 ‘trời muộn’), `light up`, `screw up`.
- u37: làm thẻ `do out` (Mini dictionary u37); u29 chỉ nhắc trong lý thuyết.
- Thêm loại trừ báo nhầm 'sách' trong `check`: *tủ sách, hiệu sách*.
- Sửa phát âm TTS: *clean/clear up after* (BATH), *pull to*, *push to* (nhấn /tuː/ cuối câu), *cast-offs* (BATH).

**Lượt 6 (Adv 41–45)**
- Không làm lại vì demo/lượt trước đã có **cùng nghĩa**: `go off`, `hanker after/for` (u41 ↔ demo u5), `deal with` (u42 ↔ demo u1), `letdown` (u42 ↔ demo u3), `drop off` ‘ngủ thiếp’ (u43 ↔ demo u2), `knock out` (u43 ↔ u20), `cut in` (u45 ↔ demo u11). Tính từ `worn out`, `tired out` (u43) đã có thẻ tính từ ở demo (u1, u4) → chỉ nhắc trong thẻ động từ `wear out`, `tire out`.
- Làm thẻ dù trùng chữ vì **khác nghĩa** (có `sense`): u41 `come over` (cảm xúc ập đến), `give in to` (cảm xúc), `summon up` (phẩm chất); u42 `get into` (đam mê), `get up to` (làm gì – u19 là ‘làm tới đâu’), `go on to` (đi tiếp đến nơi khác), `roll up` (kéo đến – u38 ‘xắn tay áo’), `take out` (dẫn đi chơi); u43 `build up`, `clear up`, `come off` (thuốc), `do in` (làm mệt lử – u29 ‘tấn công, khử’), `flare up`, `go down` (sưng), `pass on`, `pick up` (bệnh), `throw off`, `wear out` (người), `wipe out`; u44 `loosen up` (cơ bắp – u41 ‘thả lỏng tinh thần’), `spread out` (tay), `warm up` (khởi động); u45 `dry up` (nói), `run through` (giải thích – u36 ‘tiêu sạch’).
- Tính từ/danh từ phrasal gộp vào thẻ động từ thay vì làm thẻ riêng: `done in` (→ `do in`), `wiped out` (→ `wipe out`), `burnt-out` + danh từ `burnout` (→ `burn out`). `washed out`, `bunged-up` làm thẻ riêng (Mini dictionary chỉ có dạng tính từ). Xem Todo.
- Register theo chú thích trên trang khi Mini dictionary không ghi: `get up to`, `throw off`, `reel off` = informal. *Slightly informal* → `informal`: `thaw out` (trang ghi *slightly informal, metaphorical*), `bunged-up` (Mini ghi slightly informal, trang ghi informal).
- u45: `explain away` và `witter on` chỉ có trong bài tập 45.4 (+ Mini dictionary) → ví dụ đặt theo ngữ cảnh bài tập. `bombard sb with sth` pos `v.`; `engage sb in conversation` pos `phrase` (audio đọc đủ cụm).
- u44: lý thuyết có NOTE về lỗi tiểu từ (bài 44.3) và chơi chữ (bài 44.5).
- Viết lại def_en trùng Mini ≥70%: `have something against`, `work yourself into`, `pick up`, `bend down`, `stick out`, `swing around`. Viết lại ví dụ quá sát câu bài tập: `clam up`, `bend down`, `put somebody on`, `throw off`.
- Cảnh báo coverage còn lại là báo nhầm của heuristic: `pass by (swh)` (đã có thẻ `pass by`), `double (sb) over/up` (đã có `double up`, ghi chú `double over`).
- Sửa phát âm TTS: *pass by*, *pass on* (BATH /ɑː/), *bunged-up* (TTS đọc /bʌndʒd/ → /bʌŋd/).

**Lượt 7 (Adv 46 → …) – quy trình kiểm kỹ từng unit (người dùng yêu cầu: verify xong unit này mới sang unit khác)**
- Session này có 2 PDF gốc (người dùng tải lên GitHub, nhánh `main`) → `books/adv.pdf`, `books/int.pdf`; `selftest` OK (Advanced 60/60 tên unit khớp).
- Thêm `tools/review_unit.py <unit> --render` (**tùy chọn** – người dùng yêu cầu bỏ bước này vì tốn token; chỉ dùng khi nghi ngờ): in từng thẻ cạnh dòng Mini dictionary; audio (ffprobe: tồn tại, mp3, 0.4–6 s; mean_volume > −40 dB; không trùng md5); phoneme TTS cạnh IPA; render cả 2 thẻ của mọi note trong gói đã build (không `{{`, có `[sound:]` trỏ file có thật, có lý thuyết, 2 thẻ ở 2 deck nhìn/nghe).
- Thêm `tools/headwords.py <từ khoá>`: tra nhanh headword đã có (demo + units) để kiểm trùng.
- **u46 How people move** (17 mục / 34 thẻ + 1 lý thuyết): xem ảnh trang 96–97, đối chiếu từng thẻ. Lỗi `check` không bắt được, đã sửa:
  `clear out` – grammar_vi gán câu 46.2/5 cho “đội cứu hỏa” (sách: *the message warned them…*), ví dụ thêm chi tiết “thứ Sáu” (sách: cuối tuần), Common mistakes nêu nghĩa ngoài unit (*clear out the flat* = dọn dẹp) → bỏ;
  `hang back` – ví dụ thêm “chuồng hổ”, “hơi sợ” không có trong sách → bỏ; `pile into/out of` – bỏ chi tiết thêm, câu 46.1/4 (năm người, xe nhỏ); `stand back` – ví dụ đổi đúng người nói (*fire chief*), bỏ Common mistakes ngoài unit (*stand by*);
  `steal away` – “còi cảnh sát” → “xe cảnh sát” như 46.3/5; `gain on` – bỏ “slowly”; lý thuyết `creep up on` – sách chỉ nói xin lỗi vì đùa, không nói “từ phía sau/bạn giật mình”;
  đồng nghĩa sai nghĩa: `crowd out` (nghĩa thật là ‘chèn ép, loại ra’) → `leave in a rush`; `stay behind` → `not move forwards`; câu lấy từ đáp án 46.4 ghi rõ “câu gợi ý”.
  Cảnh báo còn lại: `pile into swh` (báo nhầm – heuristic coi *swh* là từ; thẻ `pile into somewhere` có); 7 cảnh báo “sách…” đều kiểm được trên ảnh trang (*informal* ở bảng B, *hung back*, *stood well back*) hoặc là chữ “sách” = books.
  Kết quả: check 0 LỖI; review 0 vấn đề; audio 17/17 (1.0–2.5 s, −20…−21 dB); render 35/35 thẻ; verify 992 note / 1934 thẻ, 0 bad renders, audio 595/595.
- **u47 Nature**: xem ảnh trang 98–99. Không làm lại vì demo đã có **cùng nghĩa**: `freeze over` (demo u2), `pick up` ‘nhặt bằng mỏ’ (demo u1/u15 ‘nhấc lên’) – chỉ nhắc trong lý thuyết. Khác nghĩa (có `sense`): `break off` (bẻ rời), `bring up` (nuôi dạy – u33 ‘nêu ra’), `come in`/`go out` (thủy triều – demo u11/u14 khác nghĩa), `come out` (sao, hoa nở), `cut down` (chặt cây), `dry up` (sông hồ cạn – u19/u45 khác), `go in` (mặt trời khuất – u24 khác), `pull up` (nhổ cây – u37 ‘kéo ghế’), `send out` (cây đâm chồi), `take over` (chiếm lãnh thổ). `eat away at something` khác `eat away at somebody` (u18). `overcast` (adj.), `offshoot` (n.) làm thẻ vì Mini dictionary gán cho u47.
  Sửa sau khi xem ảnh trang bài tập: **số bài tập ghi lệch** (đoạn phim tài liệu là 47.1, câu hỏi là 47.2 – thẻ ghi 47.2/47.3) ở 18 chỗ; ví dụ `pull up` **trái sách** (viết ‘rừng khó tái sinh’, sách: rừng luôn tự tái tạo) → đổi sang ngữ cảnh voi mục A; bỏ chi tiết tự thêm (cây non, khu rừng, gấu mẹ, sa mạc); Common mistakes nêu nghĩa ngoài unit (come up/go down cho thủy triều, die off, feed with, move on) → thay bằng lỗi suy từ dạng Mini dictionary. Ảnh trang xác nhận ‘elegant creatures’ trong 47.1 là hươu cao cổ.
- **u48 Weather**: 18 mục. `beat down` (nắng/mưa), `freeze up` (sợ/đóng băng), `mist over` (mắt) / `mist up` (kính) tách thẻ theo Mini dictionary; `fog up`, `mist up`, `steam up` 3 thẻ (3 mục Mini riêng). `roll in` sense ‘bad weather’ (u36 ‘tiền đổ về’). `breeze through` *slightly informal* → informal. Viết lại def_en `cloud over` và 2 ví dụ quá sát câu sách.
- **u49 Places**: 21 mục. Không làm lại `branch off` (demo u2 cùng nghĩa ‘đường rẽ nhánh’). Khác nghĩa: `go up` (biển báo dựng lên – u21 ‘hò reo’), `do up` (sửa sang – u25 ‘gói’), `stretch out` (vùng đất – u44 ‘duỗi’), `set off` (tôn lên). Common mistakes lấy từ bài sửa lỗi 49.2. Mini dictionary in nhầm `oak up` (= *soak up*, đã có thẻ) → cảnh báo coverage là báo nhầm.
- **u50 Transport**: 14 mục. Không làm lại `pick up` ‘đón người đi nhờ’ (demo u1/u2 ‘đón ai bằng xe’), `stowaway` (demo u3). Khác nghĩa: `branch off` (người lái rẽ khỏi đường chính – Mini u50 định nghĩa riêng), `be cast away` (dạt lên đảo – demo u1 ‘vứt bỏ’), `cut in` (lái xe chen ngang – demo u11 ‘ngắt lời’), `stack up` (máy bay chờ hạ cánh – u25 ‘chất đống’), `knock over`, `pull out`. `pick up speed` pos `phrase`. `change down`: Mini ghi *British and Australian* (vùng miền, không phải register) → neutral. Viết lại 8 ví dụ quá sát câu bài tập 50.3/50.4 hoặc có chi tiết tự thêm.
- Sửa phát âm TTS: *branch off*, *be cast away* (BATH /ɑː/), *close off* (động từ /kləʊz/, TTS đọc /kləʊs/).

**Lượt 8 (Adv 51–55)**
- Không làm lại vì demo/lượt trước đã có **cùng nghĩa**: u51 `hold out` (demo u1 ‘cầm cự’), `pick up` thông tin (u24), `sound out` (u45), `write up` (demo u15); u52 `cover up` (demo u1), `confide in` (u51); u53 `go through` (u23), `put out` (u51); u54 `back-up` (demo u3), `pick up` tín hiệu (demo u1), `set up` máy tính (demo u15 ‘chuẩn bị’); u55 `put on` weight (u26).
- Làm thẻ dù trùng chữ vì **khác nghĩa** (`sense`): u51 `call up` (nhập ngũ), `get in` (đắc cử), `get out` (tin lộ), `head off` (ngăn chặn – demo u5 ‘lên đường’), `move in` (cảnh sát vào cuộc), `pull out` (rút quân), `put down` (đàn áp), `put out` (công bố – u37 ‘đổ rác’), `shoot down` (bắn rơi – demo u6 ‘bác bỏ’), `walk out` (đình công); u52 `dig up` (khui sự thật), `give away`, `let out` (để lộ bí mật), `make out` (giả vờ); u53 `bring in` (ban hành luật), `come into` (có hiệu lực), `get through` (luật được thông qua), `let out` (thả khỏi tù), `throw out` (bác dự luật), `tighten up`, `toughen up` (luật – u40 ‘cứng cỏi’); u54 `call up` (mở thông tin), `come on`, `come up` (màn hình), `go off` (máy tắt), `go on` (lên mạng – demo u4 ‘tiếp tục’), `warm up` (máy); u55 `cut out` (kiêng), `disagree with` (đồ ăn), `soak up` (thấm hút – u49 ‘tận hưởng’), `spill over` (tràn – u28 nghĩa bóng), `wash down` (nuốt trôi – u37 ‘rửa’), `water down` 2 thẻ (đồ uống / ý kiến, theo 2 mục Mini).
- Mục Mini dictionary ghi cho unit cũ chưa có thẻ demo → làm ở unit này: `send in`, `walk out` (u51; Mini u1/u3), `print off` (u54; Mini u6), `water down` (u55; Mini u10).
- u53: `send down` chỉ có ở bài 53.4, không có trong Mini dictionary → chỉ nhắc trong lý thuyết. `abide by` register formal theo chú thích trang (Mini không ghi). u55: `(not) agree with` gộp vào thẻ `disagree with` (2 mục Mini cùng nghĩa); `water down` (ý kiến) không có ngữ cảnh trên trang ngoài Tip → ví dụ do kit đặt (xem Todo). Register theo chú thích trang: `play along`, `give-away`, `wolf down`, `fry-up` = informal.
- Sửa phát âm TTS: *give-away*, *fry-up* (trọng âm danh từ ở âm đầu), *pick at* (dạng yếu /ət/).
- Viết lại ~25 def_en trùng Mini ≥70% và ~20 ví dụ chép sát câu bài tập/đáp án (51.3, 52.2, 53.2, 55.3…), bỏ chi tiết tự thêm.

**Lượt 9 (Adv 56–60: come, get, go, keep, take)**
- Các unit này nhắc lại nhiều nghĩa đã dạy ở unit trước (sách ghi số unit) → **không làm lại**, chỉ nhắc trong lý thuyết: u56 `come across` (u40), `come at` (u20/u24), `come down` truyền đời (demo u10), `come in` thảo luận/thủy triều (demo u11, u47), `come into (being)` (u53); u57 `get around` tin đồn (demo u9), `get by` (demo u1), `get sb down` (demo u10), `get your act together` (demo u8), `get into`, `get up to` (u42), `get off` (u31); u58 `go down` hệ thống/vết sưng (demo u10, u43), `go over` (u33), `go into` (u31 `go in to`); u59 `keep down` (u21), `keep in with` (demo u5), `keep it up` (u30), `keep up` theo kịp (u24), `keep on` (demo u13); u60 `Take it away!` (u30), `take out` đi chơi (u42).
- Khác nghĩa (`sense`): `come down` (giá giảm), `come in` (phát huy vai trò), `come on` (tiến bộ), `come under` (bị công kích – u53 ‘thuộc thẩm quyền’); `get around` (đi nhiều nơi), `get in` (tranh thủ); `go after` (đuổi theo / nhắm tới), `go ahead` (sự kiện diễn ra), `go down` (kém đi), `go for` (công kích / bán được giá), `go off` (diễn ra), `go through` (trải qua); `keep up` (duy trì), `keep somebody up` (thức khuya); `take away` (đưa đi / mang về ấn tượng), `take down`, `take off` (cất cánh / nghỉ làm), `take somebody off` (thuốc / nhiệm vụ), `take out` (tiêu diệt), `take up` (nêu ra / chiếm thời gian).
- Gộp: `get away with sth` + `get away with murder` → 1 thẻ thành ngữ `get away with murder` (cùng nghĩa, bảng mục B dạy dạng *murder*). Thẻ `go after something` ghi cả dạng `go for` (Mini: *go after / for sth*). `come off better/worse` 1 thẻ.
- Không có ngữ cảnh trên trang (ví dụ do kit đặt): `take off something` (nghỉ làm – Mini u60), `take out` (tiêu diệt – chỉ có định nghĩa). `coming in` (công nghệ mới xuất hiện, u56) in đậm nhưng không có chú thích/Mini → chỉ nhắc trong lý thuyết.
- Sửa phát âm TTS: *go after* (BATH /ɑː/), *take-off* (trọng âm danh từ).

**Lượt 10 (bổ sung Advanced 1–15 cho demo)**
- Đối chiếu Mini dictionary bản 2 của từng unit 1–15 với thẻ demo và thẻ các unit khác (heuristic + đọc tay). File `units/adv_uNN.json` có `"supplement": true` → không tạo note lý thuyết, thẻ dùng lý thuyết của demo, tag `EPV::bosung_ban2`, nằm đúng deck unit của demo (đã kiểm tên deck 15/15). Helper `save_supp()` trong `tools/common.py`.
- Bổ sung: u1 (9) `breakaway, breakout, come along, cover-up, hold down, hold out for, lockout, shake-up, shutdown`; u3 (7) `break-in, downpour, lift-off, lookout, outbreak, outlook, output`; u4 (4) `fallback, left out, outstretched, worked up`; u6 (9) `ask out, back up, go into, hack into, log in, sell up, sum up (tóm tắt), take on, take over (công ty)`; u7 (4) `climb down` ×2, `warm up` ×2 (đồ ăn / khán giả); u8 (1) `wake up to the fact` (bản 2 thay *wake up and smell the coffee*); u9 (6) `blunder about, crowd around, knock somebody about, knock something about, roll about, turn around (doanh nghiệp)`; u10 (1) `take down` (ghi chép); u14 (3) `cry out, scream out, shout out`.
- Không bổ sung vì đã có thẻ cùng nghĩa: u2 (`catch up on`, `look forward to`), u5 (tất cả), u6 `scroll up/down` (demo bài bản 1), `be asking for`, `be gunning for`, `hang around`…; u7 `nose around`, `drag yourself away`, `brush off/down`; u11 `fit in with`; u15 `prop yourself up`; các mục Mini ghi cho unit sau (bail out, put out, print off, go over to, water down, send in, walk out, wear out, work out…) đã làm ở unit sau.
- **Ghi chú nguồn**: thẻ demo `hold out` (u1) dùng câu *England holds out for a draw* nhưng định nghĩa ‘cầm cự’ – Mini bản 2 xếp câu này vào `hold out for` → thêm thẻ `hold out for`, giữ thẻ demo (xem Todo). Mini u3 định nghĩa `breakout` bằng nghĩa của *outbreak* (đáp án 3.4 chọn *outbreak*) → không làm thẻ `breakout` nghĩa đó. Mini u9 `knock sth about` = ‘cân nhắc ý tưởng’ nhưng câu gợi ý Over to you dùng nghĩa ‘đá bóng qua lại’ → thẻ theo Mini, ghi chú nghĩa kia. Ví dụ do kit đặt (sách chỉ có tên bài hát/phim hoặc định nghĩa): `come along`, `hold down`, `outlook`, `hack into`, `log in`, `sell up`, `take over`, `knock somebody/something about`, `take down`.
- Sửa phát âm TTS: *cover-up, shake-up, break-in, lift-off* (trọng âm danh từ), *ask out* (BATH /ɑː/).

**Lượt 11 (Intermediate 1–10)**
- **Nguồn**: PDF Intermediate là bản scan → `src/int_*.txt` là OCR; mỗi unit xem ảnh trang (`tools/page_img.py int N both`) trước khi viết. Mini dictionary OCR lần đầu sót nhiều mục → OCR lại 300 dpi bằng tesseract (`tools/int_minidict_ocr300.txt`), parser `tools/int_minidict.py` (hợp dòng + khối) ghi lại mục MINI của 70 file src (1037 mục). Vẫn có thể sót vài mục OCR hỏng (vd. dòng `look after` u9 dính chữ) – cảnh báo "Mini chưa có thẻ" của check có dương tính giả do OCR.
- **Intermediate là sách/deck riêng**: cho phép trùng headword với Advanced (GUID có `book`). Trong cùng sách: mục có thẻ ở **unit đầu tiên** xuất hiện; unit sau chỉ nhắc trong lý thuyết ("đã có thẻ ở bài N"); nghĩa khác → thẻ mới có `sense`. Mục Mini gán cho unit sau → để unit đó.
- Mẫu ngữ pháp/helper: `PV()` trong `tools/common.py`; `check` tự sinh bảng 'Phrasal verb summary' cho lý thuyết (phải chạy check trước build).
- Int 8: `go about something` nghĩa ‘vẫn sinh hoạt thường ngày’ làm theo đáp án 8.3 (c); Mini dictionary lại ghi nghĩa ‘suốt thời gian làm điều khó chịu’ – nghĩa đó không có trong trang/bài tập → không làm thẻ. `Go on!` pos = phrase.
- Int 9: `look through` – Mini ‘đọc nhanh, không kỹ’, đáp án 9.4 nói kỹ hơn `look over` một chút → thẻ theo Mini, ghi chú cả hai. `lookout` (n.) có thẻ ở cả Adv bổ sung u3 và Int u9 (khác sách).
- Int 10: `make up` 3 nghĩa (lừa dối / sáng tác / tạo thành) + `make-up` n. (thành phần); nghĩa ‘đồ trang điểm’ chỉ nhắc trong lý thuyết (sách nói người học đã biết, không có trong Mini).
- Ví dụ: đặt trong bối cảnh trang/bài tập của unit; `tools/context_score.py` chạy từng unit, câu điểm thấp đã viết lại theo ngữ cảnh sách (vd. u6 *come down to*, u7 *can’t get over / be getting at*, u9 *lookout / look around / look through*, u10 *make up / make-up / make it up to*).

**Lượt 12 (Intermediate 11–15)**
- Mục chỉ có trong bài tập kèm định nghĩa (không có trong Mini OCR) vẫn làm thẻ khi trang/bài tập in đậm và có nghĩa: `put on` (mặc – 11.4d), `put forward` (đồng hồ – mục B), `put up` (xây/dựng lều – mục A), `eat up` (13A). Mini OCR sót các dòng này.
- Int 13: động từ `set up` (Mini 13, 49, 64) không có câu trên trang → để unit 49; chỉ làm danh từ `set-up`. Int 14: trang in đậm tính từ `worn-out` (Mini ghi động từ `wear out`) → thẻ `worn-out`, ghi động từ trong ngữ pháp. `run off` = ‘chạy đi’ (15B) chỉ nhắc, không có trong Mini.
- Thẻ trùng headword khác nghĩa có `sense`: `put off somebody` (u11 khất hẹn / u15 làm ngán), `turn off` (u2 tắt / u15 làm mất hứng), `sort out` (u1 giải quyết / u14 sắp xếp), `come out` (u6 ×4 / u14 phát hành), `take in` (u5 ×6 / u12 nhìn kỹ).

**Lượt 13 (Intermediate 16–20)**
- Int 17: `read through` chỉ có trong đáp án 17.3 → chỉ nhắc; `get over` (vượt qua) có thẻ ở đây (Mini 17, 26), khác `can’t get over` (u7).
- Int 19: `rely on / depend on / count on` ba thẻ riêng (Mini có ba mục, cùng nhóm nghĩa) – grammar ghi chú dùng như nhau. `go for` (u8 chọn / u19 cố giành) và `deal with` (nói về) có sense.
- Int 20: `call / phone / text somebody back` ba thẻ (Mini có mục riêng; `ring back` đã có ở u1); `bounce back` hai nghĩa (email / hồi phục – nghĩa sau chỉ có định nghĩa trên trang, ví dụ do kit đặt); `bite back` hai nghĩa (đáp trả / kìm lời).

**Lượt 14 (Intermediate 21–25)**
- Mục chỉ có ở bài tập kèm định nghĩa vẫn làm thẻ: `keep away` (21.4e). `be cut off` (u24 – xa xôi, biệt lập) tách khỏi `cut off sb/sth` (u2 – chặn đường); `call back` (u24 – ghé lại) tách khỏi `call sb back` (u20 – gọi điện lại); `leftover` n. (u23 – vật sót lại từ thời trước) tách khỏi `leftovers` (u4 – đồ ăn thừa); `take somebody back` (u23 – gợi nhớ).
- Thêm `tools/copy12.py`: in các cụm ≥12 từ của lý thuyết trùng src để sửa nhanh cảnh báo §3.
- Định nghĩa tiếng Anh: nhiều mục ngắn bị check báo ‘gần như chép Mini dictionary’ → viết lại toàn bộ theo lời kit (u21–u25).

**Lượt 15 (Intermediate 26–30)**
- Nghĩa mới của headword đã có thẻ → thẻ có `sense`: `pick up` (u2 đón / u26 khởi sắc / u29 nhấc lên), `give up` (u26 bỏ thói quen / u28 bỏ ngang), `take off` (u27 nổi đình đám), `keep up` (u23 tốc độ / u27 tiến bộ), `catch up` (u27 trình độ), `set out` (u4 / u28 lên đường), `break off` (u15 / u28 dừng việc), `cut down` (u17 ×2 / u28 cắt giảm), `stick with something` (u26, khác `stick with it` u19).
- u29: `email back` (Mini 29) không có trên trang → không làm thẻ.
- u30: OCR bảng mục A mất câu ví dụ → **bổ sung vào `src/int_u30.txt` mục “BỔ SUNG TỪ ẢNH TRANG”** (chép lại 3 câu từ ảnh trang 64) để collocation khớp nguồn. Áp dụng cách này cho các unit sau khi OCR mất chữ.
- `tools/copy12.py` dùng chính tokenizer của `epv.py` (trước đó lệch thuật toán, bỏ sót đoạn trùng).

## Kiểm trôi
- Lượt 15: soát Int 26–30 khi viết (ảnh trang + đáp án); viết lại câu bối cảnh tự đặt (u26 5 câu, u28 set out, u29 get down) và 1 đoạn lý thuyết u29 trùng 12 từ. Không phát hiện lệch nghĩa.
- Lượt 14: soát Int 21–25 khi viết (ảnh trang + đáp án); context_score từng unit, viết lại câu bối cảnh tự đặt (u21 burst into/buy into/tidy away, u22 while away, u23 leftover/bygone/be left over, u25 set off ×2/pay back). Không phát hiện lệch nghĩa.
- Lượt 13: soát Int 16–20 khi viết (ảnh trang + đáp án); context_score từng unit, viết lại câu bối cảnh tự đặt (u16 put on/count on/pass on, u17 load down/stay over/get over, u18 laze about/mess around/show around, u19 7 câu, u20 bite back); sửa 1 đoạn lý thuyết u20 trùng 13 từ với sách. Không phát hiện lệch nghĩa.
- Lượt 12: soát Int 11–15 khi viết (ảnh trang + đáp án); context_score từng unit, viết lại các câu bối cảnh tự đặt (u12 take apart/aside, u13 use up, u14 spread out, u15 sell off/run off ×2/put off/off-putting). Không phát hiện lệch.
- Lượt 11: soát Int 6–10 khi viết (xem ảnh trang + đáp án từng unit); kiểm lại u7 & u9: thẻ đã có ở unit trước (get on ×2, get away, get away with; look after/down on/forward to/up ×3/over/on) chỉ nhắc trong lý thuyết, không tạo thẻ trùng. Không phát hiện lệch.
- Lượt 9: kiểm u28 (ngẫu nhiên). **Lệch hệ thống như u31**: 13/19 ví dụ đặt bối cảnh tự nghĩ (thợ làm hỏng bếp, đàm phán công đoàn đổ vỡ, khách kẹt vì đình công sân bay, fan không có cúp, báo cáo đầy lỗi…) thay vì chuyện của Kate (bị dọa cắt giảm, con gái chia tay, con trai kẹt ở Phrasalia, chị gái Leo bị ung thư) và lời khuyên của Annette Berg → viết lại cả 13. **Kết luận: các lượt 2–6 viết ví dụ ‘theo nghĩa’ nhiều hơn ‘theo ngữ cảnh sách’; bước kiểm trôi cuối phải soát toàn bộ ví dụ Adv 16–45** (danh sách ưu tiên từ `tools/context_score.py`).
- Lượt 8: kiểm u18 (ngẫu nhiên) – Bethany/Toby/George mục A, hội thoại Rory/Maya bài 18.2 khớp. Sửa 2 ví dụ: `store up` (câu cũ ‘bà tích trữ hàng trăm câu chuyện gia đình’ không có trong sách → Rory: kỷ niệm đẹp mới nên cất giữ), `block out` (câu cũ gọi là ‘vụ đánh nhau’ → cảnh anh trai Anna buộc tội, xô đẩy Rory).
- Lượt 7: kiểm u31 (chọn ngẫu nhiên). **Lệch hệ thống**: 20/20 ví dụ đúng nghĩa nhưng đặt bối cảnh tự nghĩ (ly hôn, con tuổi teen, bữa trưa từ tủ lạnh, ‘Elena không hợp việc văn phòng’…) thay vì sáu người nói trong sách (sếp sắp nghỉ hưu, đại diện công đoàn, công nhân dây chuyền, trợ lý hành chính, nhà khoa học, nhân viên văn phòng) → viết lại cả 20 theo đúng ngữ cảnh sách. Thêm `tools/context_score.py`: tỉ lệ từ nội dung của ví dụ có trong src unit; u31 sau khi sửa 0/20 câu điểm thấp. Chạy cho u16–45: ~90 ví dụ điểm < 0.35 (nhiều nhất u28: 7, u25/u29/u33/u37: 5) → **TODO kiểm trôi cuối**: soát tay các câu này với src.
- Lượt 6: kiểm u23 và u26 với src. u26 khớp (email Esther, register informal của *add up/bump up/knock down*). u23: 2 ví dụ có bối cảnh tự đặt **mâu thuẫn sách** → đã sửa: `rule out` (sách: Kate bảo đừng loại Olive Bistro trước khi xem – câu cũ ‘sếp loại DJ vì đắt’ không có trong sách); `settle on` (câu cũ ‘xem ba quán, chọn rẻ nhất’ không có trong sách → nay: nhóm có đến cuối tuần để chốt địa điểm tiệc ra mắt). Chạy lại gen + check u23: 0 LỖI. Bài học: ở các lượt sau, ví dụ ‘ngữ cảnh sách’ phải dò lại chi tiết sự việc, không chỉ tên nhân vật.
- Lượt 5: kiểm u37 và u40 với src – email Abigail, các câu mục B, hội thoại Leah/Naomi, bài phát biểu chia tay Jack, đáp án 37.2/40.2; dạng tách/không tách, register khớp; không phát hiện lệch.
- Lượt 4: kiểm u31 và u35 với src – sáu người nói về công việc, tin kinh doanh và bảng collocation, đáp án 31.3/35.1/35.2; sửa 1 collocation đoán chữ bị mất trong src (`buy out one of your main rivals` – đã đối chiếu dòng sau của src). Dạng tách/không tách, register khớp.
- Lượt 3: kiểm u27 và u29 với src – nhân vật/tình huống (bài phát biểu CEO, Harry & Libby; bốn đoạn A, các hội thoại B), đáp án sửa lỗi 27.4/29.4, dạng tách/không tách, register khớp; không phát hiện lệch.
- Lượt 2: kiểm u22 và u25 với src – nhân vật/tình huống 'Mục A/B', đáp án bài tập, dạng tách/không tách, register khớp; không phát hiện lệch.
- Lượt 1b: kiểm u16 và u20 với src – bối cảnh 'Trong bài' đúng (sửa: u16 người nói là người của trường, sách không nói là hiệu trưởng → đã sửa; ví dụ u16 *hold over* bỏ chi tiết 'tháng Bảy' không có trong sách; u17 *put down to* sửa cho khớp thư của Ms Johnson). Dạng tách/không tách, register khớp Mini dictionary.

## Todo for human
- (lượt 10) Thẻ demo `hold out` (u1): định nghĩa ‘cầm cự’ nhưng ví dụ *England holds out for a draw* thuộc nghĩa `hold out for` (đã thêm thẻ riêng). Sửa ví dụ thẻ demo không?
- (lượt 9) `take off something` (nghỉ làm) và `take out` (tiêu diệt) ở u60 không có câu ngữ cảnh trong sách – ví dụ do kit đặt. Giữ hay bỏ?
- (lượt 8) `water down` nghĩa ‘làm nhẹ ý kiến/kế hoạch’ (u55): trang chỉ nhắc trong Tip, ví dụ do kit đặt. Giữ hay bỏ?
- (lượt 6) Tính từ `done in`, `wiped out`, `burnt-out` và danh từ `burnout` (u43) đang gộp vào thẻ động từ. Muốn làm thẻ riêng cho từng dạng không?
- (lượt 6) `explain away`, `witter on` (u45) chỉ xuất hiện ở bài tập 45.4 – giữ thẻ (đã giữ, vì Mini dictionary gán cho u45) hay bỏ?
- `pick up` (u24, nghĩa ‘tiếp thu thông tin/ý tưởng’): demo u1 có nghĩa ‘learn a skill/language’ khá gần. Giữ cả hai hay bỏ thẻ u24?
- `go back to sth` (u20): chỉ có trong Mini dictionary, trang sách và bài tập không có ngữ cảnh → thẻ có nghĩa đúng nhưng câu ví dụ là câu kit đặt. Giữ hay bỏ?
- Đồng/trái nghĩa: 3/191 mục không có trong src unit (vd. *calm down*, *stand up to*, *boss*) – là từ thông dụng, kiểm lại nếu muốn 100% từ sách.
- Audio: giọng TTS (Kokoro `bm_george`) khác giọng Azure của 347 thẻ demo – nghe thử vài thẻ, muốn đổi giọng thì sửa `tts_voice` rồi `epv.py audio --force`.
- 75 ví dụ demo không lấy từ sách – với chế độ tóm tắt, không cần thay (đã đóng).
- Ví dụ của thẻ demo cũ có câu chép từ sách – giữ nguyên vì là deck có sẵn của bạn; quyết định có viết lại không.
- Bản dịch tiếng Việt của 347 thẻ demo chưa được rà từng thẻ.
- Nếu đã import demo vào Anki: trước khi import bản mới, đổi tên deck `English Phrasal Verbs in Use (Advanced)` → `English Phrasal Verbs in Use::Advanced` (giữ tiến độ), vì Anki không tự chuyển thẻ cũ sang deck mới. Số unit 10–16 cũ cũng được đổi trong gói mới.
