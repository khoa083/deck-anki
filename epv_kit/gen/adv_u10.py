exec(open('tools/common.py').read())
# BỔ SUNG cho demo unit 10 Down (bản 2): Mini dictionary unit 10 có "take down sth" (ghi chép) mà demo chưa có thẻ.
# Bám sách: trang 24–25 (bài chọn cách hiểu: "I think you should take this down") + Mini dictionary. Không chép nguyên văn.
items = [
 I("take down something", "phr.v.", "neutral", "To write something down, especially what someone is saying.", "/ˌteɪk ˈdaʊn ˈsʌmθɪŋ/",
   "Viết lại điều gì, nhất là những gì ai đó đang nói.", "ghi chép lại",
   "The lecturer spoke quickly, so I tried to <b>take down</b> every word.", "Giảng viên nói nhanh nên tôi cố <b>ghi lại</b> từng chữ.",
   G("take down something", "phr.v.", "ghi lại (lời nói)", SEP("take down the address", "take the message down", "take it down"),
     "Bài tập chọn cách hiểu của unit 10: <i>I think you should take this down</i> – có thể hiểu là ‘ghi lại’ (<i>write it</i>) hoặc ‘tháo dỡ’ (<i>dismantle it</i>, xem unit 60). <i>Down</i> ở đây gợi ý đưa lời nói xuống giấy. Ví dụ trên thẻ do kit đặt.",
     "<i>take this down</i> (ghi lại cái này)", "neutral",
     "đặt đại từ sau tiểu từ (<i>take down it</i>)."),
   [S("write down", "phr.v.", "ghi xuống"), S("note down", "phr.v.", "ghi chú")], [S("forget", "v.", "quên")], sense="write"),
]
save_supp("adv", 10, items)
