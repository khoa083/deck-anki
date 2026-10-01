"""Sinh tools/books.json: tên sách, deck gốc, section (theo trang Contents), tiêu đề unit + trang PDF (theo mục lục PDF)."""
import json, os, re, pymupdf
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = {
 "ele": {"title": "English Vocabulary in Use Elementary (3rd ed.)", "root": "English Vocabulary In Use (Elementary)",
         "sections": [[1, 9, "People", "Con người"], [10, 13, "At home", "Ở nhà"], [14, 17, "School and workplace", "Trường học và nơi làm việc"],
                      [18, 26, "Leisure", "Giải trí"], [27, 33, "The world", "Thế giới"], [34, 37, "Social issues", "Vấn đề xã hội"],
                      [38, 49, "Everyday verbs", "Động từ thông dụng"], [50, 60, "Words and grammar", "Từ và ngữ pháp"]]},
 "pre": {"title": "English Vocabulary in Use Pre-intermediate and Intermediate (4th ed.)", "root": "English Vocabulary In Use (Pre-Intermediate and Intermediate)",
         "sections": [[1, 4, "Learning", "Học tập"], [5, 8, "The world around us", "Thế giới quanh ta"], [9, 15, "People", "Con người"],
                      [16, 30, "Daily life", "Cuộc sống hằng ngày"], [31, 34, "Education and study", "Giáo dục và học tập"],
                      [35, 40, "Work and business", "Công việc và kinh doanh"], [41, 45, "Leisure and entertainment", "Giải trí"],
                      [46, 51, "Tourism", "Du lịch"], [52, 55, "Communication and technology", "Giao tiếp và công nghệ"],
                      [56, 59, "Social issues", "Vấn đề xã hội"], [60, 64, "Concepts", "Khái niệm"], [65, 69, "Functional language", "Ngôn ngữ chức năng"],
                      [70, 73, "Word formation", "Cấu tạo từ"], [74, 80, "Phrase building", "Tạo cụm từ"], [81, 85, "Key verbs", "Động từ then chốt"],
                      [86, 91, "Words and grammar", "Từ và ngữ pháp"], [92, 94, "Connecting and linking", "Nối và liên kết"], [95, 100, "Style and register", "Văn phong và sắc thái"]]},
 "upp": {"title": "English Vocabulary in Use Upper-intermediate (4th ed.)", "root": "English Vocabulary In Use (Upper-Intermediate)", "demo_units": [1, 2, 3, 4, 80, 81, 82],
         "sections": [[1, 4, "Effective vocabulary learning", "Học từ vựng hiệu quả"], [5, 41, "Topics", "Chủ đề"], [42, 50, "Feelings and actions", "Cảm xúc và hành động"],
                      [51, 60, "Basic concepts", "Khái niệm cơ bản"], [61, 69, "Connecting and linking words", "Từ nối và liên kết"], [70, 79, "Word formation", "Cấu tạo từ"],
                      [80, 82, "Words and pronunciation", "Từ và phát âm"], [83, 88, "Counting people and things", "Đếm người và vật"],
                      [89, 94, "Phrasal verbs and verb-based expressions", "Cụm động từ và thành ngữ với động từ"], [95, 101, "Varieties and styles", "Biến thể và văn phong"]]},
}
for k, b in B.items():
    d = pymupdf.open(os.path.join(KIT, "books", f"{k}.pdf")); units = {}
    for lvl, t, p in d.get_toc():
        m = re.match(r"^(\d+)\s+(.*)$", t.strip())
        if m: units[m.group(1)] = {"en": m.group(2).strip(), "vi": "", "page": p - 1}   # page = chỉ số trang PDF (0-based) của trang trái
    b["units"] = units
    secs = b["sections"]; assert secs[-1][1] == len(units) and all(str(u) in units for u in range(1, len(units) + 1)), k
json.dump(B, open(os.path.join(KIT, "tools", "books.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: len(b["units"]) for k, b in B.items()})
