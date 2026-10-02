"""Thêm adv/bus/gva vào tools/books.json: unit + trang (phân tích trang Contents của sách; trang PDF = trang sách + 1), section theo Contents."""
import json, os, re, pymupdf
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(KIT, "tools", "books.json"); B = json.load(open(P, encoding="utf-8"))
def contents(book, pages):
    d = pymupdf.open(os.path.join(KIT, "books", f"{book}.pdf"))
    return d, "\n".join(d[i].get_text() for i in pages)
NEW = {
 "adv": {"title": "English Vocabulary in Use Advanced (3rd ed.)", "root": "English Vocabulary In Use (Advanced)", "cpages": [4, 5],
         "sections": [[1, 7, "Work and study", "Công việc và học tập"], [8, 15, "People and relationships", "Con người và các mối quan hệ"],
                      [16, 24, "Leisure and lifestyle", "Giải trí và lối sống"], [25, 27, "Travel", "Du lịch"], [28, 33, "The environment", "Môi trường"],
                      [34, 46, "Society and institutions", "Xã hội và thể chế"], [47, 50, "The media", "Truyền thông"], [51, 54, "Health", "Sức khỏe"],
                      [55, 58, "Technology", "Công nghệ"], [59, 71, "Basic concepts", "Khái niệm cơ bản"], [72, 84, "Functional vocabulary", "Từ vựng chức năng"],
                      [85, 91, "Words and meanings", "Từ và nghĩa"], [92, 96, "Fixed expressions and figurative language", "Cụm cố định và ngôn ngữ hình tượng"],
                      [97, 101, "Language variation", "Biến thể ngôn ngữ"]]},
 "bus": {"title": "Business Vocabulary in Use Intermediate (3rd ed.)", "root": "Business Vocabulary In Use (Intermediate)", "cpages": [4, 5, 6, 7, 8],
         "sections": [[1, 12, "Jobs, people and organizations", "Việc làm, con người và tổ chức"], [13, 18, "Production", "Sản xuất"], [19, 26, "Marketing", "Tiếp thị"],
                      [27, 34, "Money", "Tiền"], [35, 39, "Finance and the economy", "Tài chính và kinh tế"], [40, 41, "Doing the right thing", "Làm điều đúng đắn"],
                      [42, 44, "Personal skills", "Kỹ năng cá nhân"], [45, 46, "Culture", "Văn hóa"], [47, 54, "Telephoning and writing", "Gọi điện và viết"],
                      [55, 66, "Business skills", "Kỹ năng kinh doanh"]]},
 "gva": {"title": "Grammar and Vocabulary for Advanced (Hewings & Haines)", "root": "Grammar and Vocabulary for Advanced", "cpages": [5],
         "sections": [[1, 25, "Grammar", "Ngữ pháp"], [26, 45, "Vocabulary", "Từ vựng"]]},
}
for k, b in NEW.items():
    d, t = contents(k, b.pop("cpages")); t = re.sub(r"\s*\n\s*", " ", t)
    units = {}
    if k == "gva":
        for m in re.finditer(r"Unit (\d+)\s+(.+?)\s+(\d{2,3})(?= Unit| VOCABULARY| Answer)", t):
            units[m.group(1)] = {"en": m.group(2).strip(), "vi": "", "page": int(m.group(3)) + 1}
        # mục 26–28 trên trang Contents bị OCR tách cột: sửa tay theo số trang in
        for u, en, p in [(26, "Cities", 179), (27, "Personal history", 184), (28, "The arts", 188), (38, "Time off", 230)]:
            units[str(u)] = {"en": en, "vi": "", "page": p + 1}
    else:
        pos = 0
        for u in range(1, b["sections"][-1][1] + 1):
            pg = r"\d{1,3}" if k == "adv" else str(8 + 2 * u)
            m = re.compile(rf"(?<![\d.]){u} ([A-Z‘'].+?) ({pg})(?!\d)").search(t, pos)
            en, p = m.group(1).strip(), int(m.group(2)); pos = m.end()
            if k == "bus": en = re.sub(r"\s+[A-E] .*$", "", en)
            units[str(u)] = {"en": en.replace("\xa0", " ").strip(), "vi": "", "page": p + 1}
    n = b["sections"][-1][1]
    units = {str(u): units[str(u)] for u in range(1, n + 1)}
    if k == "gva":
        order = sorted(range(1, n + 1)); ans = 264
        for u in order: units[str(u)]["npages"] = (units[str(u + 1)]["page"] if u < n else ans) - units[str(u)]["page"]
    b["units"] = units; B[k] = b
json.dump(B, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k in NEW: print(k, len(B[k]["units"]), [(u, B[k]["units"][u]["en"], B[k]["units"][u]["page"]) for u in ("1", "2", str(len(B[k]["units"])))])
