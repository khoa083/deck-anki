exec(open('tools/common.py').read())
# Intermediate unit 10 – Make. Bám sách: trang 24–25 (đã xem ảnh trang) + đáp án + Mini dictionary. Không chép nguyên văn.
# make out somebody (u1), make out something/somebody = nghe/nhìn ra (u2) đã có thẻ → chỉ nhắc.
theory = (
 H("A", "Make + the particles for, out and up", "Make + các tiểu từ for, out và up")
 + T([
   ("make for somewhere", "head towards a place – e.g. children running to the swings in a park", "đi thẳng về phía một nơi – vd. lũ trẻ chạy tới xích đu trong công viên"),
   ("make out sth/sb", "manage to see or hear something, usually with difficulty (card in Unit 2)", "nhìn/nghe ra được, thường là khó khăn (đã có thẻ ở bài 2)"),
   ("make out sb", "understand why someone behaves as they do (card in Unit 1)", "hiểu được tính nết, cách cư xử của ai (đã có thẻ ở bài 1)"),
   ("make out sth", "understand something, especially why it has happened", "hiểu được điều gì, nhất là lý do nó xảy ra"),
   ("make up sth", "say or write something untrue to deceive people – e.g. an excuse", "bịa ra điều không thật để lừa – vd. một lời biện hộ"),
   ("make up sth", "invent something such as a story or a game", "nghĩ ra, sáng tác – vd. truyện, trò chơi"),
   ("make up sth", "form the whole of something – e.g. overseas students in a university", "tạo thành, chiếm – vd. sinh viên nước ngoài trong một trường đại học"),
 ])
 + P("With these three meanings, <b>make out</b> usually comes with <i>can/could</i> in a negative sentence and is not normally passive: I <i>couldn’t make out</i> what he said; I <i>can’t make</i> him <i>out</i>; I <i>can’t make out</i> why the computer won’t save my file. The noun <b>make-up</b> means cosmetics, but – from the verb <b>make up</b> – it also means the combination of things or people that form something, e.g. a class with students from many countries.",
     "Với ba nghĩa này, <b>make out</b> thường đi với <i>can/could</i> trong câu phủ định và thường không dùng bị động: tôi <i>couldn’t make out</i> anh ta nói gì; tôi <i>can’t make</i> anh ta <i>out</i>; tôi <i>can’t make out</i> vì sao máy tính không lưu được tệp. Danh từ <b>make-up</b> nghĩa là đồ trang điểm, nhưng – từ động từ <b>make up</b> – nó còn nghĩa là thành phần tạo nên một thứ, vd. một lớp học gồm sinh viên nhiều nước.")
 + H("B", "Make + two particles", "Make + hai tiểu từ")
 + T([
   ("make up for sth", "provide something good so a bad situation becomes better – e.g. great food in a restaurant with uncomfortable seats", "bù lại điều tệ bằng điều tốt – vd. đồ ăn ngon bù cho ghế ngồi khó chịu"),
   ("make it up to sb", "do something good for someone you treated badly, or who was good to you", "chuộc lỗi / đền đáp ai bằng một việc tốt"),
 ])
 + NOTE("<b>Over to you</b>: use a good dictionary, e.g. the Cambridge dictionary website, to find more phrasal verbs with <i>make</i>, and write three you want to remember in example sentences.",
        "<b>Over to you</b>: dùng một từ điển tốt, vd. trang từ điển Cambridge, để tìm thêm phrasal verb với <i>make</i>, rồi viết ba cụm bạn muốn nhớ vào câu ví dụ.")
)
items = [
 PV("make for somewhere", "phr.v.", "neutral", "To move towards a particular place.", "/ˈmeɪk fə ˈsʌmweə(r)/",
   "Di chuyển về phía một nơi nào đó.", "đi về phía, hướng tới",
   "As soon as the bell rang, the kids <b>made for</b> the playground.", "Chuông vừa reo, bọn trẻ đã <b>lao ra</b> sân chơi.",
   INS("make for the beach") + " Hay thêm <i>straight</i>: <i>make straight for the door</i>.", "Mục A: lũ trẻ chạy ngay tới xích đu khi đến công viên; bài 10.2 câu 1: nhận phòng xong là đi thẳng ra bãi biển (câu bài tập cố ý dùng sai <i>at</i>, đáp án sửa thành <i>for</i>).",
   "<i>made straight for the beach</i> (đi thẳng ra bãi biển)", "dùng <i>at</i> hoặc <i>to</i> (<i>make straight at the beach</i>).",
   [S("head for", "v.", "hướng tới"), S("go towards", "v.", "đi về phía")], [S("move away from", "v.", "rời xa")]),
 PV("make out something", "phr.v.", "neutral", "To manage to understand something, especially the reason why it has happened.", "/ˌmeɪk ˈaʊt ˈsʌmθɪŋ/",
   "Hiểu ra được điều gì, nhất là lý do nó xảy ra.", "hiểu ra, lý giải được",
   "I <b>can’t make out</b> why the printer keeps stopping halfway through a page.", "Tôi <b>không hiểu nổi</b> vì sao máy in cứ dừng giữa chừng.",
   SEP("make out the reason", "make the reason out", "make it out") + " Thường đi với <i>can’t/couldn’t</i> + <i>why/what</i>; hầu như không dùng bị động.",
   "Mục A: không hiểu sao máy tính không cho lưu tài liệu; bài 10.2 câu 3: không ai hiểu vì sao máy ảnh không chạy (câu bị động phải đổi sang chủ động).",
   "<i>can’t make out why</i> (không hiểu nổi vì sao)", "dùng bị động (<i>it could not be made out</i>).",
   [S("understand", "v.", "hiểu"), S("figure out", "phr.v.", "tìm ra")], [S("misunderstand", "v.", "hiểu nhầm")], sense="understand thing"),
 PV("make up something", "phr.v.", "neutral", "To say or write something false, such as an excuse, in order to trick someone.", "/ˌmeɪk ˈʌp ˈsʌmθɪŋ/",
   "Nói hoặc viết điều sai sự thật, như lời biện hộ, để đánh lừa ai.", "bịa ra",
   "He <b>made up</b> a story about a family emergency so he could leave work early.", "Anh ta <b>bịa ra</b> chuyện nhà có việc gấp để được về sớm.",
   SEP("make up an excuse", "make an excuse up", "make it up") + " Hay đi với <i>excuse</i>, <i>story</i>, <i>report</i>.",
   "Mục A: Katie bịa cớ ốm để khỏi đi xem hòa nhạc; bài 10.1: Logan bịa chuyện mất ví để người kia trả tiền; bài 10.2 câu 2: chuyện xe buýt đến muộn.",
   "<i>made up an excuse</i> (bịa ra một cái cớ)", "dùng <i>make out</i> (<i>she made out some story</i>).",
   [S("invent", "v.", "bịa đặt"), S("fabricate", "v.", "ngụy tạo")], [S("tell the truth", "v.", "nói thật")], sense="deceive"),
 PV("make up something", "phr.v.", "neutral", "To create a new story, game or similar thing from your imagination.", "/ˌmeɪk ˈʌp ˈsʌmθɪŋ/",
   "Tưởng tượng ra một câu chuyện, trò chơi mới.", "nghĩ ra, sáng tác",
   "On long car journeys, my mum used to <b>make up</b> word games to keep us busy.", "Trên những chuyến xe dài, mẹ tôi hay <b>nghĩ ra</b> trò chơi chữ cho chúng tôi bận rộn.",
   SEP("make up a game", "make a game up", "make it up") + " Không bao hàm ý lừa dối.",
   "Mục A: bọn trẻ quý chú Robert vì chú giỏi nghĩ ra trò chơi mới; bài 10.2 câu 4: Harry giỏi sáng tác truyện cho bọn trẻ.",
   "<i>making up new games</i> (nghĩ ra trò chơi mới)", "dùng <i>make over</i> (<i>making over stories</i>).",
   [S("invent", "v.", "sáng chế, nghĩ ra"), S("create", "v.", "tạo ra")], [S("copy", "v.", "sao chép")], sense="invent"),
 PV("make up something", "phr.v.", "neutral", "To be the parts that together form the whole of something.", "/ˌmeɪk ˈʌp ˈsʌmθɪŋ/",
   "Là các phần cùng nhau tạo nên toàn bộ một thứ.", "tạo thành, chiếm",
   "Students from abroad <b>make up</b> nearly a third of my class.", "Sinh viên nước ngoài <b>chiếm</b> gần một phần ba lớp tôi.",
   "Ở nghĩa này động từ và tiểu từ <b>không tách được</b>: <i>make up 30% of the students</i>. Hay dùng bị động <i>be made up of</i> + các thành phần.",
   "Mục A: hơn 30% sinh viên đại học là người nước ngoài; bài 10.2 câu 6: bản báo cáo gồm ba phần (đáp án: không tách <i>made … up</i>).",
   "<i>is made up of</i> (gồm có)", "tách động từ và tiểu từ (<i>is made of three sections up</i>).",
   [S("form", "v.", "hình thành"), S("comprise", "v.", "bao gồm")], [S("be excluded from", "v.", "bị loại khỏi")], sense="form"),
 PV("make-up", "n.", "neutral", "The mix of different people or things that form a group or whole.", "/ˈmeɪkʌp/",
   "Sự kết hợp các người hoặc vật khác nhau tạo nên một nhóm, một tổng thể.", "thành phần, cơ cấu",
   "Many voters were unhappy that the party’s <b>make-up</b> included so few young people.", "Nhiều cử tri không vui vì <b>thành phần</b> của đảng có quá ít người trẻ.",
   "Đây là <b>danh từ</b> không đếm được hoặc số ít, thường đi với <i>the … of</i>: <i>the make-up of the class</i>. Viết có gạch nối. Cùng gốc với <i>make up</i> (tạo thành).",
   "Mục A: lớp học có thành phần thú vị – sinh viên từ ba châu lục, 12 nước; chú thích tranh trang 25: thành phần nội các mới phản ánh cánh cực đoan của đảng. Nghĩa quen thuộc khác là đồ trang điểm.",
   "<i>an interesting make-up</i> (thành phần thú vị)", "nhầm với nghĩa ‘đồ trang điểm’ khi ngữ cảnh nói về nhóm người.",
   [S("composition", "n.", "thành phần"), S("structure", "n.", "cơ cấu")], [S("single element", "n.", "một thành phần đơn lẻ")], sense="combination"),
 PV("make up for something", "phr.v.", "neutral", "To provide something good that makes a bad situation seem less bad.", "/ˌmeɪk ˈʌp fə ˈsʌmθɪŋ/",
   "Mang lại điều tốt khiến tình huống tệ bớt tệ đi.", "bù đắp, bù lại",
   "The hotel room was tiny, but the view from the balcony <b>made up for</b> it.", "Phòng khách sạn bé tí, nhưng cảnh nhìn từ ban công đã <b>bù lại</b> tất cả.",
   INS("make up for the awful roads"), "Mục B: đồ ăn tuyệt vời bù cho ghế ngồi khá khó chịu; bài 10.1: Zara – cảnh đẹp bù cho đường xá tệ; Lars tặng quà để bù cho việc cư xử thiếu tế nhị.",
   "<i>made up for the rather uncomfortable seats</i> (bù cho ghế ngồi khó chịu)", "bỏ <i>for</i> (<i>made up the bad roads</i>).",
   [S("compensate for", "v.", "bù đắp"), S("offset", "v.", "bù trừ")], [S("make worse", "v.", "làm tệ hơn")]),
 PV("make it up to somebody", "phr.v.", "neutral", "To do something nice for someone because you have treated them badly, or because they have been kind to you.", "/ˌmeɪk ɪt ˈʌp tə ˈsʌmbədi/",
   "Làm điều tốt cho ai vì mình đã đối xử tệ với họ, hoặc vì họ đã tốt với mình.", "chuộc lỗi, đền bù cho ai",
   "I completely forgot my brother’s birthday, so I’ll <b>make it up to</b> him with a meal out.", "Tôi quên béng sinh nhật em trai, nên sẽ <b>chuộc lỗi</b> bằng một bữa ăn ngoài.",
   "Cụm cố định: <i>it</i> luôn đứng giữa <i>make</i> và <i>up</i>, người nhận đứng sau <i>to</i>: <i>make it up to her</i>.",
   "Mục B: quên sinh nhật Abigail nên phải đưa cô ấy đi đâu đó thật vui để chuộc lỗi; bài 10.1 câu 4: muốn hàn gắn một mối quan hệ.",
   "<i>make it up to her</i> (chuộc lỗi với cô ấy)", "bỏ <i>it</i> (<i>make up to her</i>).",
   [S("make amends", "v.", "sửa sai"), S("repay", "v.", "đền đáp")], [S("let down", "phr.v.", "làm thất vọng")]),
]
save("int", 10, theory, items)
