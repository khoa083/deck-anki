# STYLE GUIDE – English Phrasal Verbs in Use (Advanced + Intermediate)

Chuẩn văn phong = **thẻ demo** (xem bằng `python3 epv.py demo adv 2`). Nguồn sự thật = **sách PDF bản 2** (src/ + ảnh trang).
Mọi thứ ghi "theo sách" phải kiểm được trong `src/<book>_uNN.txt` hoặc ảnh trang. Không có trong sách → không viết như thể sách nói.

## 0. Chế độ BÁM SÁCH – DIỄN GIẢI (từ lượt 1b, 2026-10-01), ghi đè mọi dòng khác
**Bám sách 100%, không chép nguyên văn, không bịa.** Mọi thông tin trên thẻ phải truy được về src/ảnh trang của **chính unit đó** (trang lý thuyết, bài tập, đáp án, Mini dictionary).
- **Lý thuyết**: theo đúng từng mục A/B/C của sách. Mỗi mục: 1 câu nêu bối cảnh của sách (ai, chuyện gì), rồi bảng `T()` – mỗi phrasal verb + nghĩa của nó **trong đoạn đó** (diễn đạt lại chú thích đánh số của sách) + tiếng Việt. Mẹo/Tip/ghi chú của sách và các ý rút từ bài tập/đáp án đưa vào `NOTE()`. Không thêm kiến thức ngoài sách. Không chép câu/đoạn của sách (`check` cảnh báo ≥ 12 từ liên tiếp trùng).
- **def_en**: nghĩa Mini dictionary diễn đạt lại (`check` cảnh báo trùng ≥ 70%).
- **example.en**: câu tự đặt nhưng **trong ngữ cảnh của sách** (nhân vật, tình huống, collocation của unit), không chép và không diễn đạt sát một câu của sách (`check` cảnh báo trùng ≥ 60%; tự rà cả câu bài tập có chỗ trống vì `check` không thấy được).
- **grammar_vi**: dùng `G()` + `SEP/INS/INT`. Phần ghi chú: "Mục A/B…: …", "Bài tập 16.3: …" – nêu ngữ cảnh sách. **Collocations** chỉ lấy cụm có trong src unit (`check` kiểm). **Common mistakes** ưu tiên lỗi trong bài tập sửa lỗi của sách + lỗi vị trí đại từ suy từ dạng Mini dictionary. Không nêu nghĩa khác ngoài unit (trừ khi sách nêu, ví dụ đáp án 18.3 nói *call up* = gọi nhập ngũ, hoặc nghĩa ở unit khác của cùng sách).
- **Đồng/trái nghĩa** (field bắt buộc): ưu tiên phrasal verb của cùng unit, từ trong định nghĩa/chú thích sách, phương án đáp án ghi "also possible", cụm sách dùng để diễn giải trong bài tập viết lại câu. `check` in tỉ lệ không có trong src.
- Mục Mini dictionary **không có ngữ cảnh** trên trang/bài tập → vẫn làm thẻ theo nghĩa, ghi rõ trong grammar_vi và *Todo for human*.
- Mục trùng **cùng nghĩa** với thẻ demo → không làm lại. Khác nghĩa → làm, đặt `sense`. Thẻ demo cũ giữ nguyên.
- Mẫu chuẩn: `gen/adv_u16.py` … `gen/adv_u20.py`.

## 1. File unit (units/<book>_uNN.json) – viết bằng gen/<book>_uNN.py

```python
exec(open('tools/common.py').read())
theory = H("A", "How time passes", "Thời gian trôi qua như thế nào") + " " + BOXED(en, vi) + " " + P(en, vi) + " " + table(...)
items = [I(word, pos, register, def_en, ipa, def_vi, gloss_vi, ex_en, ex_vi, grammar_vi, [S(..), S(..)], [S(..)], sense="")]
save("adv", 16, theory, items)
```
Sau đó `python3 epv.py check adv_u16` (tự thêm bảng *Phrasal verb summary* cuối lý thuyết).

Unit **bổ sung** cho demo (Advanced 1–15, thêm mục bản 2 mà demo thiếu): `{"book":"adv","unit":6,"supplement":true,"theory_html":"","items":[...]}` – không tạo note lý thuyết mới, thẻ dùng lý thuyết của demo.

## 2. Từng field (mỗi mục = 1 note = 2 thẻ)

| JSON | Field Anki | Quy tắc |
|---|---|---|
| `word` | Từ vựng | Dạng gốc như Mini dictionary của sách, đổi `sb/sth` → `somebody/something` (như demo): *knock down*, *set aside something*, *hit on something*. Danh từ/tính từ phrasal viết đúng như sách (*stand-off*, *worn out*). |
| `sense` | (GUID) | Để trống. Chỉ điền nhãn ngắn tiếng Anh khi **cùng word có nhiều nghĩa trong cùng unit** (demo unit 1 có 10 thẻ *pick up*). |
| `pos` | trong Định nghĩa (a) | Chỉ dùng: `phr.v.` · `n.` · `adj.` · `idiom` · `phrase` · `v.` |
| `register` | (QA) | `neutral` / `formal` / `informal` / `very informal` – theo nhãn của sách (Mini dictionary ghi *formal*, *informal*…); không có nhãn → `neutral`. Phải khớp câu Register trong grammar_vi. |
| `def_en` | Định nghĩa (a) | 1 câu tiếng Anh **bằng lời mình**, đúng nghĩa Mini dictionary của unit đó, kết thúc bằng dấu chấm. Chỉ nghĩa được dạy trong unit này. |
| `ipa` | IPA | `/…/`, **chuẩn Anh** (RP): əʊ, e, ɒ, ɑː, không r sau nguyên âm trước phụ âm, có trọng âm ˈ ˌ. Giữ `somebody /ˈsʌmbədi/`, `something /ˈsʌmθɪŋ/`. |
| `def_vi` | Định nghĩa (v) | Dịch sát nghĩa def_en, tự nhiên, kết thúc bằng dấu chấm. |
| `gloss_vi` | Dịch nghĩa | Nghĩa ngắn (≤ 8 từ), chữ thường, đúng nghĩa trong unit. |
| `example.en` | Câu ví dụ hoàn chỉnh | **1 câu đặt trong ngữ cảnh của sách** (§0), không chép câu sách, bôi đậm phrasal verb bằng `<b>`. |
| `example.vi` | Dịch câu ví dụ | Dịch cả câu, bôi đậm phần dịch của phrasal verb bằng `<b>`. |
| `synonyms` | Đồng nghĩa | 2 mục `S(text, pos, vi)` → hiển thị `demolish <i>(v. phá dỡ)</i>, tear down <i>(phr.v. phá bỏ)</i>`. Phải cùng nghĩa với **nghĩa đang dạy**. |
| `antonyms` | Trái nghĩa | 1–2 mục, cùng định dạng. Không có trái nghĩa thật → dùng cụm đối lập hợp lý nhất, KHÔNG lặp lại mục đồng nghĩa. |
| `grammar_vi` | Ngữ pháp | 80–240 từ, khung cố định (bên dưới). |
| (tự sinh) | STT, Nguồn, Bài giảng lý thuyết | `016`, rỗng (đã bỏ chữ “Anki Support Vietnam” theo yêu cầu), lý thuyết của unit. **Phát âm** = `[sound:epv_<book>_u<NN>_<slug>.mp3]`, build tự gắn từ `media/` (tạo bằng `epv.py audio`). Thiếu file = LỖI. |

### Khung grammar_vi (bắt buộc có **Grammar** và **Register**)
```
<i>knock down</i> (phr.v.) = phá dỡ/làm đổ một công trình. <b>Grammar</b>: Đây là phrasal verb <b>ngoại động từ</b> …
<b>tách được</b>: <i>knock the old hotel down</i>; với <b>đại từ</b> phải đặt giữa: <i>knock it down</i>. [nghĩa trong bài khác nghĩa nào] …
<b>Collocations / chunks</b>: <i>knock down a building/wall</i> (phá tòa nhà/tường) …
<b>Register</b>: trung tính, dùng tốt trong nói và viết. <b>Common mistakes</b>: đặt sai vị trí đại từ (knock down it) …
```
Thông tin ngữ pháp (tách được / không tách được, có tân ngữ hay không, vị trí đại từ) **lấy theo sách**: Mini dictionary ghi
`knock down sth or knock sth down` = tách được; `look after sb` (không có dạng tách) = không tách; `come up` (không có sth/sb) = nội động từ.
Unit 2 (Advanced) và unit 1 (Intermediate) giải thích quy ước này.

### Thẻ chuẩn (lấy từ demo)
- Từ vựng: `knock down` · Định nghĩa (a): `<i>phr.v.</i> To destroy a building or structure by hitting it so that it falls, or by demolishing it.`
- IPA: demo sau chuẩn hoá là `/nɒk daʊn/`; **thẻ mới ghi đủ trọng âm**: `/ˌnɒk ˈdaʊn/` · Định nghĩa (v): `Phá dỡ một tòa nhà hoặc công trình bằng cách làm nó đổ xuống.` · Dịch nghĩa: `phá dỡ`
- Câu ví dụ: `They’re <b>knocking down</b> the old hotel.` · Dịch: `Họ đang <b>phá dỡ</b> khách sạn cũ.`
- Trái nghĩa: `build up <i>(phr.v. xây dựng)</i>, put up <i>(phr.v. dựng lên)</i>` · Đồng nghĩa: `demolish <i>(v. phá dỡ)</i>, tear down <i>(phr.v. phá bỏ)</i>`

## 3. Lý thuyết (theory_html)
- Giữ **khung mục** của sách: A/B/C… với tiêu đề như sách (`H("A", en, vi)`); unit không có mục → 1 mục A mang tên chủ đề. Nội dung: `P()` bối cảnh của sách, `T()` từng phrasal verb + nghĩa trong đoạn, `NOTE()` mẹo/ghi chú của sách và bài tập. Mẫu: `gen/adv_u16.py`–`adv_u20.py`.
- Phần tiếng Anh **diễn giải sát nội dung sách** (§0), in đậm phrasal verb. Không chép câu/đoạn của sách, không thêm ý ngoài sách.
- Bản dịch tiếng Việt in nghiêng ngay dưới, dịch đủ ý, không thêm giải thích ngoài sách. Không đưa bài tập (trang phải) vào lý thuyết.
- Ảnh trong sách: không chép ảnh; nếu ảnh mang nội dung (chú thích), ghi phần chữ.

## 4. Thuật ngữ tiếng Việt (dùng thống nhất – theo demo)
| English | Tiếng Việt |
|---|---|
| phrasal verb | phrasal verb (giữ nguyên) |
| particle | tiểu từ |
| transitive / intransitive | ngoại động từ / nội động từ |
| object | tân ngữ |
| separable / inseparable | tách được / không tách được |
| phrasal noun / phrasal adjective | danh từ phrasal / tính từ phrasal |
| register | phong cách ngôn ngữ (register) |
| formal / informal / neutral | trang trọng / thân mật / trung tính |
| literal / metaphorical meaning | nghĩa đen / nghĩa ẩn dụ (nghĩa bóng) |
| idiom | thành ngữ |
| collocation | collocation (giữ nguyên) |

## 5. Tiếng Việt
Dịch đúng nghĩa trước, rồi mới tới tự nhiên. Không dịch word-by-word gượng; không diễn giải thoáng tới mức đổi nghĩa.
Không mở câu bằng "Nó"; nói rõ chủ ngữ. Không để sót từ tiếng Anh ngoài `<i>`/`<b>`. Dấu câu và dấu tiếng Việt đầy đủ.
