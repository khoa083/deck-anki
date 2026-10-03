# Deck gộp theo bộ sách

Chỉ import các APKG cấp bộ nằm ngay trong `dist/` vào Anki. Các APKG đơn lẻ nằm trong `dist/individual/` là bản nguồn/dự phòng; đừng import cả hai nơi cùng lúc.

## Grammar in Use.apkg

- `01 Essential Grammar In Use (Elementary)`
- `02 English Grammar In Use (Intermediate)`
  - `01 Main Book`
  - `02 Supplementary Exercises`
- `03 Advanced Grammar In Use`

Kết quả verify: 15,073 notes/cards; 0 bad renders; 0 GUID trùng; 0 media thiếu.

## English Vocabulary In Use.apkg

- `01 Elementary (A2)`
- `02 Pre-Intermediate and Intermediate (B1)`
- `03 Upper-Intermediate (B2)`
- `04 Advanced (C1-C2)`
- `05 Academic Vocabulary in Use (B2-C1, source deck)`

Kết quả verify: 10,304 notes / 20,227 cards; 0 bad renders; 0 GUID trùng; 0 media thiếu. Academic là deck nguồn nguyên bản có trong `main` (759 notes), chưa phải bản được biên soạn/Việt hoá theo pipeline EVU.

## English Phrasal Verbs in Use.apkg

Đổi tên file từ `EPV_full.apkg`; nội dung đã là một deck có nhánh Advanced và Intermediate. Không thay đổi collection bên trong.

## Business Vocabulary In Use.apkg

- `01 Intermediate (B1-B2)`

Repo hiện chỉ có bản Intermediate; Cambridge có bản Advanced cùng series nhưng PDF nguồn chưa có trong `main`.

## Sách vẫn để riêng

- `Grammar and Vocabulary for Advanced.apkg`: sách luyện thi độc lập, không thuộc Grammar in Use.

Không tạo một gói “tất cả sách” vì việc gộp các họ sách khác nhau sẽ làm thứ tự học và nội dung từng series khó nhận biết.
