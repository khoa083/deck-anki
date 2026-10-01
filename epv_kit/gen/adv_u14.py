exec(open('tools/common.py').read())
# BỔ SUNG cho demo unit 14 Out (bản 2): Mini dictionary unit 14 có cry out / scream out / shout out (cùng định nghĩa với yell out – thẻ demo).
# Đáp án unit 14 ghi: ‘heard somebody yell out from the staircase below’ – shout out / cry out / scream out cũng dùng được. Không chép nguyên văn.
def SH(word, past, ipa, vi_gloss, vi_verb, ex_en, ex_vi, extra):
    return I(word, "phr.v.", "neutral", "To suddenly call out something loudly, especially to get someone’s attention.", ipa,
      "Bất ngờ nói to điều gì, nhất là để gây sự chú ý của ai.", vi_gloss, ex_en, ex_vi,
      G(word, "phr.v.", vi_verb, "Mini dictionary ghi <i>" + word.split()[0] + " out (sth) or " + word.split()[0] + " (sth) out</i>: dùng không tân ngữ (<i>someone " + past + " out</i>) hoặc có tân ngữ, tách được với đại từ.",
        "Đáp án unit 14: câu ‘tôi mở cửa và nghe ai đó hét lên từ cầu thang bên dưới’ dùng <i>yell out</i> (thẻ demo), và sách ghi <i>shout out / cry out / scream out</i> cũng dùng được. " + extra,
        "<i>" + word.split()[0] + " out from the staircase</i> (hét lên từ cầu thang)", "neutral",
        "quên <i>out</i> khi muốn nhấn mạnh hành động bật ra đột ngột."),
      [S("yell out", "phr.v.", "hét lên"), S("call out", "phr.v.", "gọi to")], [S("whisper", "v.", "thì thầm")])
items = [
 SH("cry out", "cried", "/ˌkraɪ ˈaʊt/", "kêu lên", "kêu to", "From the bottom of the stairs, someone <b>cried out</b> for help.", "Từ chân cầu thang, ai đó <b>kêu lên</b> cầu cứu.", "Unit 14: tiểu từ <i>out</i> ở đây gợi âm thanh phát ra to, ra ngoài."),
 SH("scream out", "screamed", "/ˌskriːm ˈaʊt/", "thét lên", "thét to", "When I opened the door, I heard someone <b>scream out</b> on the staircase.", "Khi mở cửa, tôi nghe ai đó <b>thét lên</b> ở cầu thang.", "Ba động từ có cùng định nghĩa trong Mini dictionary."),
 SH("shout out", "shouted", "/ˌʃaʊt ˈaʊt/", "hô to, la lên", "la to", "Someone on the stairs below <b>shouted out</b> my name.", "Ai đó ở cầu thang bên dưới <b>gọi to</b> tên tôi.", "Ba động từ có cùng định nghĩa trong Mini dictionary."),
]
save_supp("adv", 14, items)
