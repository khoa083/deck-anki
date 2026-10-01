"""Helper cho gen/<book>_uNN.py. Dùng:  exec(open('tools/common.py').read())  rồi save("adv", 16, theory, items)."""
import json, os, re
_KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if "__file__" in globals() else "."
BOX = '<div style="background-color: rgb(229, 241, 251); padding: 10px; border-radius: 8px; margin-bottom: 10px;">'

def H(letter, en, vi):
    """Tiêu đề mục: A. English / A. Tiếng Việt"""
    return f"<p><b>{letter}. {en}</b></p> <p><i>{letter}. {vi}</i></p>"

def P(en, vi):
    """Đoạn song ngữ: câu gốc của sách (giữ <b> cho phrasal verb) + bản dịch in nghiêng."""
    return f"<p>{en}</p> <p><i>{vi}</i></p>"

def BOXED(en, vi):
    """Khung xanh cho đoạn văn / hội thoại / email của sách (giống demo)."""
    return f"{BOX}<p>{en}</p> <p><i>{vi}</i></p></div>"

def table(head_en, head_vi, rows):
    """rows: [(cột1_en, cột1_vi, cột2_en, cột2_vi, ...)] – mỗi ô: en + <br><i>vi</i>"""
    th = "".join(f"<th>{e}<br><i>{v}</i></th>" for e, v in zip(head_en, head_vi))
    tr = ""
    for r in rows:
        cells = [r[i:i + 2] for i in range(0, len(r), 2)]
        tr += "<tr>" + "".join(f"<td>{e}" + (f"<br><i>{v}</i>" if v else "") + "</td>" for e, v in cells) + "</tr>"
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"

def S(text, pos, vi):
    """Phần tử synonyms/antonyms. pos: 'phr.v.' | 'v.' | 'n.' | 'adj.' | 'adv.' | 'idiom' | 'phr.'"""
    return {"text": text, "pos": pos, "vi": vi}

def I(word, pos, register, def_en, ipa, def_vi, gloss_vi, ex_en, ex_vi, grammar_vi, synonyms, antonyms, sense=""):
    """Một mục từ vựng (1 note = 2 thẻ). sense: nhãn ngắn tiếng Anh khi cùng word có nhiều nghĩa trong 1 unit."""
    return {"word": word, "sense": sense, "pos": pos, "register": register, "def_en": def_en, "ipa": ipa,
            "def_vi": def_vi, "gloss_vi": gloss_vi, "example": {"en": ex_en, "vi": ex_vi},
            "grammar_vi": grammar_vi, "synonyms": synonyms, "antonyms": antonyms, "audio": ""}

def save(book, unit, theory, items):
    out = os.path.join(_KIT, "units", f"{book}_u{unit:02d}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"book": book, "unit": unit, "theory_html": theory, "items": items}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved", out, len(items), "items")

# ---------------------------------------------------------------- chế độ TÓM TẮT (từ lượt 1, xem STYLE_GUIDE §0)
REG = {"neutral": "trung tính, dùng được cả khi nói và viết.",
       "formal": "hơi trang trọng, hợp với văn viết, báo cáo, thư từ, bài luận.",
       "informal": "thân mật, chủ yếu dùng khi nói chuyện thường ngày.",
       "very informal": "rất thân mật, chỉ nên dùng với người quen."}

def SEP(a, b, pron):
    """Ngoại động từ, tách được."""
    return (f"Đây là phrasal verb <b>ngoại động từ</b> và <b>tách được</b>: tân ngữ đứng sau cả cụm (<i>{a}</i>) "
            f"hoặc giữa động từ và tiểu từ (<i>{b}</i>); nếu tân ngữ là <b>đại từ</b> thì bắt buộc đặt giữa: <i>{pron}</i>.")

def INS(ex):
    """Có tân ngữ nhưng không tách được."""
    return (f"Đây là phrasal verb <b>không tách được</b>: tân ngữ luôn đứng sau cả cụm, kể cả khi là đại từ: <i>{ex}</i>.")

def INT(ex):
    """Nội động từ."""
    return f"Đây là phrasal verb <b>nội động từ</b>, không cần tân ngữ: <i>{ex}</i>, nên không có dạng tách."

def G(word, pos, nghia, gram, note, coll, register, mist):
    """Khung grammar_vi chuẩn. note = điểm phân biệt/ghi nhớ thêm (1–2 câu)."""
    return (f"<i>{word}</i> ({pos}) = {nghia}. <b>Grammar</b>: {gram} {note} "
            f"<b>Collocations / chunks</b>: {coll}. <b>Register</b>: {REG.get(register, register)} "
            f"<b>Common mistakes</b>: {mist}")

def NOTE(en, vi):
    """Khung ghi nhớ ngắn trong lý thuyết (tóm tắt bằng lời của mình, KHÔNG chép sách)."""
    return BOXED(en, vi)

def T(rows, head=("Phrasal verb", "Meaning in this text", "Nghĩa trong bài")):
    """Bảng lý thuyết bám sách: rows = [(phrasal verb, nghĩa en diễn đạt lại, nghĩa vi)]."""
    return table([head[0], head[1]], [head[0], head[2]], [(pv, "", en, vi) for pv, en, vi in rows])
