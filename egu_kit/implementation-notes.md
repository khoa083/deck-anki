# implementation-notes – English Grammar in Use (egu_kit)

## Tiến độ
| Sách (key) | Nguồn | Unit | Trạng thái |
|---|---|---|---|
| English Grammar in Use 5th ed. (Intermediate) | deck mẫu `base/English Grammar In Use (Intermediate).apkg` (145 unit) | 145 | giữ nguyên nội dung; chỉ xuất lại bản đã bỏ chữ "Anki Support Vietnam" (`tools/clean_sample.py`) |
| Essential Grammar in Use 4th ed. (ess) | `books/ess.pdf` (bản digital) | 115 | **xong 115/115** |
| Advanced Grammar in Use 3rd ed. (agu) | `books/agu.pdf` | 100 | **xong 100/100** |
| Supplementary Exercises (sup) | `books/sup.pdf` (EGU Intermediate, 200 bài) | 32 nhóm | **xong**; MCQ gắn với lý thuyết Intermediate theo `@egu` |

| Deck | Kết quả đo (`egu.py verify`) |
|---|---|
| Essential Grammar In Use (Elementary) | 4658 note / 4658 thẻ (115 unit theory + 4536 MCQ + 7 appendix theory); bad renders 0; GUID trùng 0; MCQ logic trùng 11 (xem dưới); còn chữ thương hiệu 0 |
| Advanced Grammar In Use | 3715 note / 3715 thẻ (100 lý thuyết + 3615 MCQ); bad renders 0; GUID trùng 0; MCQ logic trùng 0; còn chữ thương hiệu 0 |
| English Grammar In Use Supplementary Exercises | 1719 note / 1719 thẻ (32 lý thuyết + 1687 MCQ); bad renders 0; GUID trùng 0; MCQ logic trùng 0; còn chữ thương hiệu 0 |
| English Grammar In Use (Intermediate) (mẫu) | 4981 note; đã bỏ link thương hiệu ở 3 template + giá trị `AnkiSupportVietnam` ở trường Nguồn của 4479 note; còn 0 |

## Quy trình
`data/<book>_uNNN.txt` (viết tay, song ngữ) → `tools/compile.py` → `units/<book>_uNNN.json` → `tools/build_deck.py` → `out/<Root>.apkg`.
CLI: `python3 egu.py make|check|build|verify|status <book> [từ] [đến]`.
- `src/<book>_uNNN.txt`: văn bản trích từ PDF (lý thuyết, bài tập, đáp án) – chỉ để đối chiếu khi viết `data/`.
- Note type & giao diện lấy nguyên từ deck mẫu: `Tóm tắt++` (lý thuyết) và `MCQ custom shuffled (Grammar)` (câu hỏi). Cây deck: `<Root>::A. Lý thuyết::NN-Section::Unit` và `<Root>::B. Câu hỏi::NN-Section::Unit`, như mẫu.
- GUID cố định `egu|book|unit|__theory__` và `egu|book|unit|câu hỏi|đáp án` → import lại chỉ cập nhật, không nhân đôi.
- `build_deck.py` gọi `strip_brand` trước khi xuất; `SOURCE = ""` (trường Nguồn để trống).

## Chính sách nội dung
- **Chỉ dùng sách làm nguồn.** Câu MCQ lấy từ ví dụ lý thuyết, câu bài tập và đáp án (Key) của chính unit đó; lý thuyết là bản song ngữ bám sát các mục A/B/C… của trang.
- Khi Key ghi "both possible" / "also possible", phương án còn lại **không bao giờ** được dùng làm phương án sai; dùng dạng sai rõ ràng thay thế. Đã rà từng unit để bỏ các phương án sai nhưng vẫn đúng ngữ pháp (vd. *should/must*, *a/one*, *since/because*, *Except for*, *amongst*, *seeing as*…).
- Câu có nhiều chỗ trống: đáp án nối bằng " … "; đáp án "–" = để trống.
- Bản dịch VI luôn có phần **[đậm]** tương ứng chỗ trống; không dùng "[–]".
- Validate khi build: lý thuyết ≥ 300 ký tự, ≥ 15 MCQ/unit, thẻ HTML cân, `<b>` có trong câu hoàn chỉnh (trừ đáp án "–") và trong bản dịch.

## Deviations
- **agu – văn bản PDF bị mã hoá dịch ký tự**: một số đoạn bài tập trong `agu.pdf` trích ra bị dịch +3 (vd. `IURPKLVRI¿FH` = *from his office*). Đã giải mã bằng dịch −3 và đối chiếu với Key trước khi dùng.
- **ess – 11 MCQ logic trùng giữa các unit**: sách lặp lại cùng câu ở các unit khác nhau (cùng câu, cùng đáp án). Giữ lại vì mỗi câu gắn với điểm ngữ pháp của unit đó; GUID vẫn khác nhau theo unit nên không trùng note.
- **Phụ lục ess**: 7 appendix có note lý thuyết song ngữ ngắn gọn (chủ động/bị động, động từ bất quy tắc, dạng rút gọn, chính tả, cụm động từ). Nguồn biên soạn: phụ lục sách Essential Grammar in Use 4th ed.; nội dung là ghi chú học tập cô đọng, không chép nguyên bảng dài. Nguồn dữ liệu `data/ess_appendices.json`; compile bằng `python tools/compile_appendices.py` ra `units/ess_aNN.json`.
- **Sup liên kết lý thuyết**: mỗi nhóm bài có `egu_units`; build kiểm tra mọi unit tham chiếu đều có trong deck mẫu Intermediate và đưa phần lý thuyết vào mặt sau ghi chú MCQ.
- Một số câu trong Key chỉ là "Possible answers" (bài viết tự do): chỉ dùng phần cố định của câu trả lời mẫu; không tự đặt câu mới.

## Todo for human
- Phụ lục agu chưa được bổ sung; ngoài phạm vi đợt này.
- 11 MCQ ess trùng logic giữa các unit được giữ lại vì sách lặp lại câu hỏi theo các điểm ngữ pháp khác nhau.
