from flask import Flask, request, render_template_string
import re

app = Flask(__name__)


FONTS = [
    {'name': 'Bold', 'upper': '𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉', 'lower': '𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣', 'digits': '𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝟶'},
    {'name': 'Italic', 'upper': '𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁', 'lower': '𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛', 'digits': '1234567890'},
    {'name': 'Bold Italic', 'upper': '𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕', 'lower': '𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯', 'digits': '1234567890'},
    {'name': 'Slim Italic', 'upper': '𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡', 'lower': '𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻', 'digits': '1234567890'},
    {'name': 'Monospace', 'upper': '𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭', 'lower': '𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇', 'digits': '𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬'},
    {'name': 'Bold Mono', 'upper': '𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙', 'lower': '𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳', 'digits': '𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎'},
    {'name': 'Superscript', 'upper': 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻ', 'lower': 'ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖqʳˢᵗᵘᵛʷˣʸᶻ', 'digits': '¹²³⁴⁵⁶⁷⁸⁹⁰'},
    {'name': 'Small Caps', 'upper': 'ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢ', 'lower': 'ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢ', 'digits': '1234567890'},
    {'name': 'Fullwidth', 'upper': 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ', 'lower': 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ', 'digits': '１２３４５６７８９０'},
    {'name': 'Double Struck', 'upper': '𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ', 'lower': '𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫', 'digits': '𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘'},
    {'name': 'Cursive', 'upper': 'ꪖ᥇ᥴᦔꫀᠻᧁꫝⅈ𝕛𝕜ꪶꪑꪀꪮρ𝕢𝕣ડ𝕥ꪊꪜ᭙᥊ꪗ𝕫', 'lower': 'ꪖ᥇ᥴᦔꫀᠻᧁꫝⅈ𝕛𝕜ꪶꪑꪀꪮρ𝕢𝕣ડ𝕥ꪊꪜ᭙᥊ꪗ𝕫', 'digits': '𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘'},
    {'name': 'Script', 'upper': '𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵', 'lower': '𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏', 'digits': '𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢'},
    {'name': 'Bold Script', 'upper': '𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩', 'lower': '𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃', 'digits': '1234567890'},
    {'name': 'Mixed Style', 'upper': '☢★  𝐀𝒷ᑕ𝔻є𝔽Ğ𝒽ιⒿᵏ𝐋ⓜήσ𝓅Ω𝕣𝓈ＴⓊV𝔀𝓍𝓨乙', 'lower': 'α𝕓𝔠∂𝔼Ŧ𝕘𝐡𝕚ⓙкℓ𝐦Ｎⓞ𝓟𝓠𝓻ᔕт𝕦ᵛｗｘㄚⓏ', 'digits': '➀➁❸❹❺➅７８➈ʘ'},
    {'name': 'Fancy', 'upper': '✌♞𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪℘𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵', 'lower': '𝒶𝒷𝒸𝒹ℯ𝒻ℊℎ𝒾𝒿𝓀ℓ𝓂𝓃ℴ℘𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝒴𝓏', 'digits': '𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟫𝟶'},
    {'name': 'Fraktur', 'upper': '𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅', 'lower': '𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟', 'digits': '1234567890'},
    {'name': 'Bold Fraktur', 'upper': '𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ', 'lower': '𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷', 'digits': '1234567890'},
    {'name': 'Circled', 'upper': 'ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ', 'lower': 'ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ', 'digits': '①②③④⑤⑥⑦⑧⑨⓪'},
    {'name': 'Parenthesis', 'upper': '⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵', 'lower': '⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵', 'digits': '⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽'},
    {'name': 'Squared', 'upper': '🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉', 'lower': '🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉', 'digits': '🄀🄁🄂🄃🄄🄅🄆🄇🄈🄉'},
    {'name': 'Regional', 'upper': '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿', 'lower': '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿', 'digits': '0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣'},
    {'name': 'Gothic', 'upper': '𝔊𝔬𝔱𝔥𝔦𝔠 𝔖𝔱𝔶𝔩𝔢', 'lower': '𝔤𝔬𝔱𝔥𝔦𝔠 𝔰𝔱𝔶𝔩𝔢', 'digits': '1234567890'},
    {'name': 'Handwriting', 'upper': '𝓗𝓪𝓷𝓭𝔀𝓻𝓲𝓽𝓲𝓷𝓰', 'lower': '𝓱𝓪𝓷𝓭𝔀𝓻𝓲𝓽𝓲𝓷𝓰', 'digits': '1234567890'},
    {'name': 'Tiny', 'upper': 'ᵀⁱⁿʸ ᵀᵉˣᵗ', 'lower': 'ᵗⁱⁿʸ ᵗᵉˣᵗ', 'digits': '¹²³⁴⁵⁶⁷⁸⁹⁰'},
    {'name': 'Upside Down', 'upper': '∀qƆpƎℲ⅁H⇂ſʞ˥WNOԀQɹS┴∩ΛMX⅄Z', 'lower': 'ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz', 'digits': '⥝⥞⥟⥠⥡⥢⥣⥤⥥⥦'},
    {'name': 'Mirror', 'upper': 'ZYXWVUTSRQPONMLKJIHGFEDCBA', 'lower': 'zyxwvutsrqponmlkjihgfedcba', 'digits': '0987654321'},
    {'name': 'Wide', 'upper': 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ', 'lower': 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ', 'digits': '１２３４５６７８９０'},
    {'name': 'Bold Wide', 'upper': '𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭', 'lower': '𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇', 'digits': '𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬'},
    {'name': 'Italic Wide', 'upper': '𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡', 'lower': '𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻', 'digits': '1234567890'},
]


def convert_to_font(text, font_data):
    result = []
    for char in text:
        if 'A' <= char <= 'Z':
            idx = ord(char) - ord('A')
            result.append(font_data['upper'][idx] if idx < len(font_data['upper']) else char)
        elif 'a' <= char <= 'z':
            idx = ord(char) - ord('a')
            result.append(font_data['lower'][idx] if idx < len(font_data['lower']) else char)
        elif '0' <= char <= '9':
            idx = ord(char) - ord('0')
            result.append(font_data['digits'][idx] if idx < len(font_data['digits']) else char)
        else:
            result.append(char)
    return ''.join(result)


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✨ فونت‌ساز BalehroonHelper</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazir:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Vazir', Tahoma, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        /* انیمیشن پس‌زمینه */
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 30% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 70% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
            animation: rotate 20s linear infinite;
            z-index: 0;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .container {
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            padding: 50px;
            max-width: 1000px;
            width: 100%;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6);
            transition: all 0.3s ease;
        }
        
        /* هدر */
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 50px;
            margin-bottom: 10px;
            display: inline-block;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        h1 {
            color: #fff;
            font-size: 32px;
            font-weight: 900;
            letter-spacing: 1px;
        }
        
        h1 span {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            color: rgba(255, 255, 255, 0.6);
            font-size: 14px;
            margin-top: 8px;
            letter-spacing: 2px;
        }
        
        /* جعبه ورودی */
        .box {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 35px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.3s ease;
        }
        
        .box:hover {
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        label {
            display: block;
            color: rgba(255, 255, 255, 0.8);
            font-size: 16px;
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        .input-group {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 16px 20px;
            background: rgba(255, 255, 255, 0.06);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            font-size: 18px;
            color: #fff;
            transition: all 0.3s ease;
            direction: ltr;
            text-align: left;
            min-width: 200px;
        }
        
        input[type="text"]::placeholder {
            color: rgba(255, 255, 255, 0.3);
        }
        
        input[type="text"]:focus {
            border-color: #764ba2;
            outline: none;
            box-shadow: 0 0 0 4px rgba(118, 75, 162, 0.2);
            background: rgba(255, 255, 255, 0.1);
        }
        
        button {
            padding: 16px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Vazir', Tahoma, sans-serif;
            white-space: nowrap;
        }
        
        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(118, 75, 162, 0.4);
        }
        
        button:active {
            transform: translateY(0px);
        }
        
        /* خطا */
        .error {
            color: #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
            padding: 14px 20px;
            border-radius: 12px;
            border-right: 4px solid #ff6b6b;
            margin-top: 18px;
            font-weight: 700;
            display: {% if error %}flex{% else %}none{% endif %};
            align-items: center;
            gap: 10px;
        }
        
        .error::before {
            content: '🚫';
            font-size: 20px;
        }
        
        /* نتیجه */
        .result {
            margin-top: 30px;
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .result-header h3 {
            color: #fff;
            font-size: 22px;
            font-weight: 700;
        }
        
        .result-header .count-badge {
            background: rgba(102, 126, 234, 0.3);
            color: #fff;
            padding: 6px 18px;
            border-radius: 50px;
            font-size: 14px;
            border: 1px solid rgba(102, 126, 234, 0.3);
        }
        
        /* کارت‌های فونت */
        .font-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }
        
        .font-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 16px 20px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s ease;
            direction: ltr;
            text-align: left;
            cursor: pointer;
            flex-wrap: wrap;
        }
        
        .font-item:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(102, 126, 234, 0.3);
            transform: translateX(5px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        }
        
        .font-number {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 3px 10px;
            border-radius: 50%;
            font-size: 11px;
            font-weight: 700;
            min-width: 28px;
            text-align: center;
            flex-shrink: 0;
        }
        
        .font-name {
            background: rgba(255, 255, 255, 0.08);
            color: rgba(255, 255, 255, 0.7);
            padding: 3px 14px;
            border-radius: 50px;
            font-size: 12px;
            font-weight: 700;
            flex-shrink: 0;
            letter-spacing: 0.5px;
        }
        
        .font-text {
            flex: 1;
            color: #fff;
            font-size: 22px;
            word-break: break-all;
            min-width: 100px;
            font-family: 'Segoe UI', Tahoma, sans-serif;
            direction: ltr;
        }
        
        .copy-btn {
            background: rgba(255, 255, 255, 0.08);
            color: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 6px 16px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.3s ease;
            font-family: 'Vazir', Tahoma, sans-serif;
            flex-shrink: 0;
        }
        
        .copy-btn:hover {
            background: rgba(102, 126, 234, 0.3);
            color: #fff;
            border-color: #667eea;
            transform: scale(1.05);
        }
        
        .copy-btn.copied {
            background: rgba(46, 213, 115, 0.3);
            color: #2ed573;
            border-color: #2ed573;
        }
        
        /* فوتر */
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 25px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            color: rgba(255, 255, 255, 0.3);
            font-size: 13px;
            letter-spacing: 1px;
        }
        
        .footer span {
            color: #ff6b6b;
        }
        
        /* انیمیشن ورود */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .font-item {
            animation: fadeInUp 0.5s ease forwards;
            opacity: 0;
        }
        
        .font-item:nth-child(1) { animation-delay: 0.05s; }
        .font-item:nth-child(2) { animation-delay: 0.10s; }
        .font-item:nth-child(3) { animation-delay: 0.15s; }
        .font-item:nth-child(4) { animation-delay: 0.20s; }
        .font-item:nth-child(5) { animation-delay: 0.25s; }
        .font-item:nth-child(6) { animation-delay: 0.30s; }
        .font-item:nth-child(7) { animation-delay: 0.35s; }
        .font-item:nth-child(8) { animation-delay: 0.40s; }
        .font-item:nth-child(9) { animation-delay: 0.45s; }
        .font-item:nth-child(10) { animation-delay: 0.50s; }
        .font-item:nth-child(11) { animation-delay: 0.55s; }
        .font-item:nth-child(12) { animation-delay: 0.60s; }
        .font-item:nth-child(13) { animation-delay: 0.65s; }
        .font-item:nth-child(14) { animation-delay: 0.70s; }
        .font-item:nth-child(15) { animation-delay: 0.75s; }
        .font-item:nth-child(16) { animation-delay: 0.80s; }
        .font-item:nth-child(17) { animation-delay: 0.85s; }
        .font-item:nth-child(18) { animation-delay: 0.90s; }
        .font-item:nth-child(19) { animation-delay: 0.95s; }
        .font-item:nth-child(20) { animation-delay: 1.00s; }
        .font-item:nth-child(21) { animation-delay: 1.05s; }
        .font-item:nth-child(22) { animation-delay: 1.10s; }
        .font-item:nth-child(23) { animation-delay: 1.15s; }
        .font-item:nth-child(24) { animation-delay: 1.20s; }
        .font-item:nth-child(25) { animation-delay: 1.25s; }
        .font-item:nth-child(26) { animation-delay: 1.30s; }
        .font-item:nth-child(27) { animation-delay: 1.35s; }
        .font-item:nth-child(28) { animation-delay: 1.40s; }
        .font-item:nth-child(29) { animation-delay: 1.45s; }
        .font-item:nth-child(30) { animation-delay: 1.50s; }
        
        /* ریسپانسیو */
        @media (max-width: 768px) {
            .container {
                padding: 25px;
            }
            
            h1 {
                font-size: 22px;
            }
            
            .logo {
                font-size: 35px;
            }
            
            .box {
                padding: 20px;
            }
            
            .input-group {
                flex-direction: column;
            }
            
            button {
                width: 100%;
                justify-content: center;
            }
            
            .font-item {
                padding: 12px 15px;
                gap: 8px;
            }
            
            .font-text {
                font-size: 18px;
                min-width: 80px;
            }
            
            .font-name {
                font-size: 10px;
            }
            
            .result-header h3 {
                font-size: 18px;
            }
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 15px;
            }
            
            .font-text {
                font-size: 15px;
                min-width: 60px;
            }
            
            .copy-btn {
                font-size: 11px;
                padding: 4px 12px;
            }
        }
        
        /* اسکرول بار سفارشی */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2, #667eea);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- هدر -->
        <div class="header">
            <div class="logo">🎨</div>
            <h1>سلام به فونت‌ساز انگلیسی <span>BalehroonHelper</span></h1>
            <div class="subtitle">✨ ۳۰ فونت خاص برای متن‌های انگلیسی شما</div>
        </div>
        
        <!-- جعبه ورودی -->
        <div class="box">
            <form method="POST" id="fontForm">
                <label>📝 لطفا متن انگلیسی را وارد کنید:</label>
                <div class="input-group">
                    <input type="text" 
                           name="text" 
                           id="textInput"
                           placeholder="مثلاً: Hello World 123" 
                           value="{{ request.form.get('text', '') }}" 
                           required
                           autofocus>
                    <button type="submit">✨ تبدیل کن</button>
                </div>
                
                <div class="error">{{ error }}</div>
            </form>
        </div>
        
        <!-- نتیجه -->
        {% if fonts %}
        <div class="result">
            <div class="result-header">
                <h3>🔥 {{ fonts|length }} فونت خاص برای شما</h3>
                <span class="count-badge">🎯 {{ fonts|length }} فونت</span>
            </div>
            
            <div class="font-grid">
                {% for font in fonts %}
                <div class="font-item" id="font-{{ loop.index }}">
                    <span class="font-number">{{ loop.index }}</span>
                    <span class="font-name">{{ font.name }}</span>
                    <span class="font-text" id="text-{{ loop.index }}">{{ font.text }}</span>
                    <button class="copy-btn" onclick="copyText('{{ font.text|e }}', {{ loop.index }})">
                        📋 کپی
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        <!-- فوتر -->
        <div class="footer">
            ساخته شده با <span>♥</span> توسط BalehroonHelper
        </div>
    </div>
    
    <script>
        function copyText(text, index) {
            // روش مدرن
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(function() {
                    showCopied(index);
                }).catch(function() {
                    // روش قدیمی
                    fallbackCopy(text, index);
                });
            } else {
                // روش قدیمی
                fallbackCopy(text, index);
            }
        }
        
        function fallbackCopy(text, index) {
            var textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            textarea.style.left = '-9999px';
            document.body.appendChild(textarea);
            textarea.select();
            
            try {
                var successful = document.execCommand('copy');
                if (successful) {
                    showCopied(index);
                } else {
                    alert('❌ کپی نشد! لطفاً دستی کپی کنید.');
                }
            } catch (err) {
                alert('❌ کپی نشد! لطفاً دستی کپی کنید.');
            }
            
            document.body.removeChild(textarea);
        }
        
        function showCopied(index) {
            var btn = document.querySelector('#font-' + index + ' .copy-btn');
            var originalText = btn.textContent;
            btn.textContent = '✅ کپی شد!';
            btn.classList.add('copied');
            
            setTimeout(function() {
                btn.textContent = originalText;
                btn.classList.remove('copied');
            }, 2000);
        }
        
        // کپی با کلیک روی کل آیتم
        document.querySelectorAll('.font-item').forEach(function(item) {
            item.addEventListener('click', function(e) {
                // اگر روی دکمه کپی کلیک نشده بود
                if (!e.target.classList.contains('copy-btn')) {
                    var textSpan = this.querySelector('.font-text');
                    var btn = this.querySelector('.copy-btn');
                    if (textSpan) {
                        copyText(textSpan.textContent, 
                                this.id.replace('font-', ''));
                    }
                }
            });
        });
        
        // فوکوس خودکار روی اینپوت
        document.addEventListener('DOMContentLoaded', function() {
            var input = document.getElementById('textInput');
            if (input && !input.value) {
                input.focus();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    fonts = []
    
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        
        if not text:
            error = '⚠️ لطفاً متنی وارد کنید.'
        elif re.search(r'[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF]', text):
            error = '🔴 کلمه شما حاوی حروف فارسی میباشد، لطفا اصلاح کنید.'
        else:
            for font_data in FONTS:
                converted = convert_to_font(text, font_data)
                fonts.append({
                    'name': font_data['name'],
                    'text': converted
                })
    
    return render_template_string(HTML_TEMPLATE, error=error, fonts=fonts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
