import os
import re

# 1. DỮ LIỆU THÔ ĐƯỢC ĐỊNH NGHĨA TRONG CODE

SUMMARY_CONTENT = """
- [「～だらけ、～おかげ、～せい」](01-darake-okage-sei.md)
- [「～について、～に関して」](02-tsuite-nikanshite.md)
- [「ぽい、みたい、ように、ような」](03-poi-mitai-youni-youna.md)
- [「～みたいだ、～らしい」](04-mitaida-rashii.md)
- [「比べて、加えて、対して」](05-kurabete-kuwaete-taishite.md)
- [「たびに、たとえ～ても」](06-tabini-tatoe-temo.md)
- [「って」](07-tte.md)
- [「くらい、ぐらい」](08-kurai-gurai.md)
- [「～くらいなら、～うちに」](09-kurainara-uchini.md)
- [「～を中心に、～を始め」](10-wochuushinni-wohajime.md)
- [「～において、～にわたって／～にわたる」](11-nioite-niwatatte.md)
- [「～にとって、～に違いない」](12-nitotte-nichigainai.md)
- [「～とは、～たとたん」](13-toha-tatotan.md)
- [「つれて、したがって」](14-tsurete-shitagatte.md)
- [「～て以来、～一方だ」](15-teirai-ippouda.md)
- [「～しかない／～ほかない、～はもちろん、～ついでに」](16-shikanai-hokanai-tsuideni.md)
- [「～ということだ、～ことはない、～こと」](17-toiukotoda-kotohanai-koto.md)
- [「～ないことは（も）ない、もの（もん）、ものだから」](18-naikotohamonai-monodakara.md)
- [「ものか、～たところ、～ところに」](19-monoka-tatokoro-tokoroni.md)
- [「ほど①②③④」](20-hodo.md)
- [「～ほど～はない、～ば～ほど」](20-2-hodohanai-bahodo.md)
- [「～からには、～ぎみ、～がち」](21-karaniwa-gimi-gachi.md)
- [「向け／向き、～を通して／～を通じて」](22-muke-muki-wotooshite.md)
- [「～に決まっている、～きる、～きれる」](23-nikimatteiru-kiru-kireru.md)
- [「～とともに、～にともない／ともなって」](24-totomoni-nitomonai.md)
- [「～てある、～ておく、～てしまう、～ていく、～てくる」](25-tearu-teoku-teshimau-teiku-tekuru.md)
- [「～ようになる、～ようにする、～ことになる、～ことにする」](26-youninaru-younisuru-kotoninaru-kotonisuru.md)
- [「～ようと思う、～つもり、～予定」](27-you-to-omou-tsumori-yotei.md)
- [「～てみる」](28-temiru.md)
- [「～始める、～続ける、～終わる」](29-hajimeru-tsuzukeru-owaru.md)
- [「～ために」](30-tameni.md)
- [「～そうだ（様態）、～そうだ（伝聞）」](31-souda-youtai-denbun.md)
- [「～最中、～間、～間に"](32-saichuu-aida-aidani.md)
- [「～たり～たり、～とか」](33-tari-tari-toka.md)
"""

YOUTUBE_LINKS = [
    "https://www.youtube.com/watch?v=flfi38e0NKk",  # #1
    "https://www.youtube.com/watch?v=p5V-Q5hH8e0",  # #2
    "https://www.youtube.com/watch?v=s1cgzbLVkTg",  # #3
    "https://www.youtube.com/watch?v=Krk34qYUQeE",  # #4
    "https://www.youtube.com/watch?v=JO7zsq2uY_s",  # #5
    "https://www.youtube.com/watch?v=hrefMxfxBJc",  # #6
    "https://www.youtube.com/watch?v=Vx_dCXVv324",  # #7
    "https://www.youtube.com/watch?v=A2xqiuXc9D8",  # #8
    "https://www.youtube.com/watch?v=AO46Nu7dbuk",  # #9
    "https://www.youtube.com/watch?v=414K4PxSw4E",  # #10
    "https://www.youtube.com/watch?v=wKmjdwDFfBY",  # #11
    "https://www.youtube.com/watch?v=Lh1mDGVY3Gw",  # #12
    "https://www.youtube.com/watch?v=MEnkZfln8FA",  # #13
    "https://www.youtube.com/watch?v=lukMSDKohbw",  # #14
    "https://www.youtube.com/watch?v=Ym3NGIZ0Q6Q",  # #15
    "https://www.youtube.com/watch?v=65KbZioDfJ4",  # #16
    "https://www.youtube.com/watch?v=_9CsetnMH6A",  # #17
    "https://www.youtube.com/watch?v=F9SnRS-MgKs",  # #18
    "https://www.youtube.com/watch?v=WaxlDufwGAU",  # #19
    "https://www.youtube.com/watch?v=VkxDlk8P5aE",  # #20
    "https://www.youtube.com/watch?v=qaJznD0GSuQ",  # #20-2
    "https://www.youtube.com/watch?v=tNUgnQfPKXE",  # #21
    "https://www.youtube.com/watch?v=o7CyB444ybc",  # #22
    "https://www.youtube.com/watch?v=-gb6FiW-R1M",  # #23
    "https://www.youtube.com/watch?v=RR4luTbjpOM",  # #24
    # 9 video cuối được sắp xếp lại dựa trên liên kết text thô cuối đề bài của bạn:
    "https://www.youtube.com/watch?v=qXqKfwBlGgc",  # 25 (~てある...)
    "https://www.youtube.com/watch?v=4qRSVPNeIuw",  # 26 (~ようになる...)
    "https://www.youtube.com/watch?v=fq5oXIr7iYM",  # 27 (~ようと思う...)
    "https://www.youtube.com/watch?v=RT6nJy_sius",  # 28 (てみる)
    "https://www.youtube.com/watch?v=dq545ol5lKA",  # 29 (~始める...)
    "https://www.youtube.com/watch?v=i5KxU8XbUGI",  # 30 (~ために)
    "https://www.youtube.com/watch?v=vULsJo_QGaw",  # 31 (~そうだ...)
    "https://www.youtube.com/watch?v=LqxDq2EsH20",  # 32 (~最中...)
    "https://www.youtube.com/watch?v=2FtPWz9KJBo",  # 33 (~たり～たり...)
]

def main():
    # Thư mục đích chứa các bài học, đổi tên tùy theo dự án SSG của bạn
    output_dir = "n3-grammar"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Sử dụng Regex để trích xuất Title và File Name từ SUMMARY.md
    pattern = re.compile(r'-\s+\[(.*?)\]\((.*?)\)')
    lines = SUMMARY_CONTENT.strip().split('\n')
    
    lessons = []
    for line in lines:
        match = pattern.search(line)
        if match:
            title = match.group(1)
            file_name = match.group(2)
            lessons.append((title, file_name))
            
    # Kiểm tra số lượng bài học và video khớp nhau không
    if len(lessons) != len(YOUTUBE_LINKS):
        print(f"⚠️ Cảnh báo: Số bài học ({len(lessons)}) khác số lượng video ({len(YOUTUBE_LINKS)})!")

    # Tiến hành sinh tệp
    for i, (title, file_name) in enumerate(lessons):
        # Lấy link youtube tương ứng hoặc để trống nếu vượt chỉ mục
        youtube_url = YOUTUBE_LINKS[i] if i < len(YOUTUBE_LINKS) else ""
        
        file_path = os.path.join(output_dir, file_name)
        
        # Định dạng cấu trúc Frontmatter cho hệ thống SSG hochanh
        markdown_template = f"""---
title: "{title}"
youtube: {youtube_url}
---

Hãy viết nội dung bài học cho **{title}** tại đây...
"""
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_template)
            
        print(f"✅ Đã tạo: {file_path}")

    print(f"\n🎉 Hoàn thành! Toàn bộ tệp bài học đã nằm tại thư mục `{output_dir}/`.")

if __name__ == "__main__":
    main()