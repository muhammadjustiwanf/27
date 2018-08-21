# Script By @Adi
# Please Don’t Edit If You Doesn’t Have A Permission.
# © Adi, 2018 All Rights Reserved.

from gtts import gTTS
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from googletrans import Translator
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from humanfriendly import format_timespan, format_size, format_number, format_length

from flask import Flask, request, make_response

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib3, urllib.parse, traceback, atexit, html5lib, wikipedia, goslate

app = Flask(__name__)

line_bot_api = LineBotApi('HjEZRNk3czUVKof7ZLxIO3Bv8zdkeW1UBTPl9HNMmYgVHtQapRJr2ZyVB8qOMVrdmkTDfZ7nRjnavXF8xgO9qeBVd47MSgfP3k0J+oPWjw8+8dli+crm5VKHcFi+xidY2razYmls+0EC9CxIYnbOYwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a4ce4df86f3b49ce0ab0a91f1f4fec16')

list_language = {
    "list_textToSpeech": {
        "id": "Indonesia",
        "af" : "Afrikaans",
        "sq" : "Albanian",
        "ar" : "Arabic",
        "hy" : "Armenian",
        "bn" : "Bengali",
        "ca" : "Catalan",
        "zh" : "Chinese",
        "zh-cn" : "Chinese (Mandarin/China)",
        "zh-tw" : "Chinese (Mandarin/Taiwan)",
        "zh-yue" : "Chinese (Cantonese)",
        "hr" : "Croatian",
        "cs" : "Czech",
        "da" : "Danish",
        "nl" : "Dutch",
        "en" : "English",
        "en-au" : "English (Australia)",
        "en-uk" : "English (United Kingdom)",
        "en-us" : "English (United States)",
        "eo" : "Esperanto",
        "fi" : "Finnish",
        "fr" : "French",
        "de" : "German",
        "el" : "Greek",
        "hi" : "Hindi",
        "hu" : "Hungarian",
        "is" : "Icelandic",
        "id" : "Indonesian",
        "it" : "Italian",
        "ja" : "Japanese",
        "km" : "Khmer (Cambodian)",
        "ko" : "Korean",
        "la" : "Latin",
        "lv" : "Latvian",
        "mk" : "Macedonian",
        "no" : "Norwegian",
        "pl" : "Polish",
        "pt" : "Portuguese",
        "ro" : "Romanian",
        "ru" : "Russian",
        "sr" : "Serbian",
        "si" : "Sinhala",
        "sk" : "Slovak",
        "es" : "Spanish",
        "es-es" : "Spanish (Spain)",
        "es-us" : "Spanish (United States)",
        "sw" : "Swahili",
        "sv" : "Swedish",
        "ta" : "Tamil",
        "th" : "Thai",
        "tr" : "Turkish",
        "uk" : "Ukrainian",
        "vi" : "Vietnamese",
        "cy" : "Welsh"
    },
    "list_translate": {    
        "af": "afrikaans",
        "sq": "albanian",
        "am": "amharic",
        "ar": "arabic",
        "hy": "armenian",
        "az": "azerbaijani",
        "eu": "basque",
        "be": "belarusian",
        "bn": "bengali",
        "bs": "bosnian",
        "bg": "bulgarian",
        "ca": "catalan",
        "ceb": "cebuano",
        "ny": "chichewa",
        "zh-cn": "chinese (simplified)",
        "zh-tw": "chinese (traditional)",
        "co": "corsican",
        "hr": "croatian",
        "cs": "czech",
        "da": "danish",
        "nl": "dutch",
        "en": "english",
        "eo": "esperanto",
        "et": "estonian",
        "tl": "filipino",
        "fi": "finnish",
        "fr": "french",
        "fy": "frisian",
        "gl": "galician",
        "ka": "georgian",
        "de": "german",
        "el": "greek",
        "gu": "gujarati",
        "ht": "haitian creole",
        "ha": "hausa",
        "haw": "hawaiian",
        "iw": "hebrew",
        "hi": "hindi",
        "hmn": "hmong",
        "hu": "hungarian",
        "is": "icelandic",
        "ig": "igbo",
        "id": "indonesian",
        "ga": "irish",
        "it": "italian",
        "ja": "japanese",
        "jw": "javanese",
        "kn": "kannada",
        "kk": "kazakh",
        "km": "khmer",
        "ko": "korean",
        "ku": "kurdish (kurmanji)",
        "ky": "kyrgyz",
        "lo": "lao",
        "la": "latin",
        "lv": "latvian",
        "lt": "lithuanian",
        "lb": "luxembourgish",
        "mk": "macedonian",
        "mg": "malagasy",
        "ms": "malay",
        "ml": "malayalam",
        "mt": "maltese",
        "mi": "maori",
        "mr": "marathi",
        "mn": "mongolian",
        "my": "myanmar (burmese)",
        "ne": "nepali",
        "no": "norwegian",
        "ps": "pashto",
        "fa": "persian",
        "pl": "polish",
        "pt": "portuguese",
        "pa": "punjabi",
        "ro": "romanian",
        "ru": "russian",
        "sm": "samoan",
        "gd": "scots gaelic",
        "sr": "serbian",
        "st": "sesotho",
        "sn": "shona",
        "sd": "sindhi",
        "si": "sinhala",
        "sk": "slovak",
        "sl": "slovenian",
        "so": "somali",
        "es": "spanish",
        "su": "sundanese",
        "sw": "swahili",
        "sv": "swedish",
        "tg": "tajik",
        "ta": "tamil",
        "te": "telugu",
        "th": "thai",
        "tr": "turkish",
        "uk": "ukrainian",
        "ur": "urdu",
        "uz": "uzbek",
        "vi": "vietnamese",
        "cy": "welsh",
        "xh": "xhosa",
        "yi": "yiddish",
        "yo": "yoruba",
        "zu": "zulu",
        "fil": "Filipino",
        "he": "Hebrew"
    }
}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = (event.message.text).lower()
    msg = text.split()
    groupId = event.source.group_id
    userId = event.source.user_id
    profile = line_bot_api.get_profile(userId)
    profile_name = profile.display_name
    profile_picture = profile.picture_url
    profile_sm = profile.status_message


    if text == '.samehadaku':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Harap bersabar, " + profile_name + " :v")
        target = 'https://samehadaku.tv'
        req = requests.get(target)
        bs = BeautifulSoup(req.content, "html.parser")
        dataa = bs.find_all("ul",{"class":"posts-items posts-list-container"})
        dataaa = dataa[0].find_all("li",{"class":"post-item tie-standard"})
        content = "[ RESULT ]\n~ Last Update Anime: Samehadaku ~\n\n\n"
        num = 0
        for data in dataaa:
            num += 1
            data = dataaa[1].find('a')
            date = dataaa[1].find('span').text
            name = data["title"]
            link = data["href"]
            time = date
            content += "{}).  Judul: {}".format(num, name)
            content += "\n       Link: {}".format(link)
            content += "\n       Tanggal Rilis: {}\n\n".format(time)
            te = "\n✓ Total ada {} update anime.\n✓ Info update anime selengkapnya, klik:\n➡ https://www.samehadaku.tv/".format(len(dataaa))
            line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(text=content+te)])


    elif text == '.toramnews':
        target = 'https://en.toram.jp/information/?type_code=all'
        req = requests.get(target)
        bs = BeautifulSoup(req.content, "html.parser")
        dataa = bs.find_all("div",{"class":"useBox"})
        dataaa = dataa[0].find_all("li")
        content = "~ Toram Online Official News ~\n\n\n"
        num = 0
        i = 0

        for data in dataaa:
            num += 1
            if i <= 9:
                pass

            data = dataaa[i].find('a')
            news = data.text
            link = data["href"]
            tx = "✓ Total ada {} berita.\n\n\n✓ Info selengkapnya, klik:\n➡ https://en.toram.jp/information/?type_code=all".format(len(dataaa))
            i = i + 1

            content += "{}). News: {}\n      More info: https://en.toram.jp{}\n\n".format(num, news, link)

        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage(text="[ R E S U L T ]\n\nBot using by [ "+profile_name+" ] on Toram News:\n\n"+content+tx)])

        return

    elif text == '.pic':
        target_url = 'https://www.ptt.cc/bbs/Beauty/index.html'
        res = requests.get(target_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        pic_urls = []

        while (len(pic_urls) < 1):
            for data in soup.select('.r-ent'):
                pushes = data.select_one('.nrec').text
                if pushes == '爆' or (pushes != '' and 'X' not in pushes and int(pushes) > 50):
                    title = data.find('a', href=True)
                    heading = title.text
                    link = 'https://www.ptt.cc' + title['href']

                    if '公告' in heading:
                        continue

                    res2 = requests.get(link)
                    soup2 = BeautifulSoup(res2.text, 'html.parser')

                    for data2 in soup2.select_one('#main-content').find_all('a', href=True):
                        if 'https://i.imgur.com' in data2['href']:
                            pic_urls.append(data2['href'])

                    break

            last_page_url = 'https://www.ptt.cc' + soup.select('.btn.wide')[1]['href']
            res = requests.get(last_page_url)
            soup = BeautifulSoup(res.text, 'html.parser')

        image_message = ImageSendMessage(
            original_content_url=random.choice(pic_urls),
            preview_image_url=random.choice(pic_urls)
        )

        line_bot_api.reply_message(
            event.reply_token,
            image_message
        )
        return


    elif text == '.joke':
        url_req = requests.get('https://raw.githubusercontent.com/abhishtagatya/dlearn-res/master/dotPython/interact/bot_interact.json')
        reply_mes = url_req.json()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(reply_mes["joke"])))


    elif text == '.bye':
        if (userId != 'U45a70016f56dbfc99e6a66673002ecbe'):
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Akses Ditolak! Hanya owner yang bisa menggunakan command ini."))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Sayounara, "+profile_name+"........................"))
            line_bot_api.leave_group(groupId)


    elif text == '.userid':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hai "+profile_name+", ini adalah id kamu: "+userId))


    elif text == '.myprofile':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="~ [ RESULT ] ~\n\n👉 Nama: "+profile_name+"\n👉 Foto Profil: "+profile_picture+"\n👉 Pesan Status: "+profile_sm))


    if '.apakah ' in text:
        rep = text.replace(".apakah ","")
        txt = ["Ya","Tidak","Bisa Jadi","Mungkin","Hoax","Coba tanya lagi"]

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(txt)))


    elif '.carigambar' in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        source = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(search))
        data = source.text
        data = json.loads(data)

        if data["result"] != []:
            items = data["result"]
            path = random.choice(items)
            a = items.index(path)
            b = len(items)

        image_message = ImageSendMessage(
            original_content_url=path,
            preview_image_url=path
        )

        line_bot_api.reply_message(
            event.reply_token,
            image_message
        )


    elif '.zodiak ' in text:
        tanggal = text.replace(".zodiak ","")
        r = requests.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=siapa&tanggal='+tanggal)
        data = r.text
        data = json.loads(data)
        lahir = data["data"]["lahir"]
        usia = data["data"]["usia"]
        ultah = data["data"]["ultah"]
        zodiak = data["data"]["zodiak"]

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="[ RESULT ]\n\n"+"Tanggal: "+lahir+"\nUsia: "+usia+"\nUltah: "+ultah+"\nZodiak: "+zodiak+"\n\n[ FINISH ]"))


    elif '.wiki ' in text:
        try:
            wiki = text.replace(".wiki ","")
            wikipedia.set_lang("id")
            results = wiki.find("search")
            pesan = "~ [ R E S U L T ] ~\n\nBot using by [ "+profile_name+"  ] in Wikipedia Search Engine.\n\n\n👉 Nama: "
            pesan += wikipedia.page(wiki).title
            pesan += "\n\n👉 Deskripsi: "
            pesan += wikipedia.summary(wiki, sentences=1)
            pesan += "\n\n👉 Baca Selengkapnya: "
            pesan += wikipedia.page(wiki).url
            pesan += "\n\n\n✓ Baca wikipedia lainnya klik:\n➡ https://id.wikipedia.org/"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=pesan))

        except:
                try:
                    pesan="Over Text Limit! Please Click link\n"
                    pesan+=wikipedia.page(wiki).url
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=pesan))
                except Exception as e:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=e))


    elif '.lokasi' in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        req = requests.get("https://time.siswadi.com/pray/{}".format(search))
        data = req.text
        data = json.loads(data)
        add = data['location']['address']
        lat = data['location']['latitude']
        lon = data['location']['longitude']

        location_message = LocationSendMessage(
            title='Lokasi',
            address=add,
            latitude=lat,
            longitude=lon
        )

        line_bot_api.reply_message(
            event.reply_token,
            location_message
        )


    elif 'meet?' in text:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message
        )


    elif ".carilagu " in text:
        separate = text.split(" ")
        query = text.replace(separate[0] + " ","")
        cond = query.split(":")
        search = cond[0]
        source = requests.get("http://api.ntcorp.us/joox/search?q={}".format(search))
        data = source.text
        data = json.loads(data)
        if len(cond) == 1:
            num = 0
            ret_ = "[ SEARCH RESULT ]"
            for music in data["result"]:
                num += 1
                ret_ += "\n\n~ {}. {}".format(num, music["single"])
            ret_ += "\n\n[ TOTAL: {} MUSIK ]".format(len(data["result"]))
            ret_ += "\n\nUntuk melihat detail musik, silahkan gunakan command:\n.carilagu {}:「number」\nContoh: .carilagu {}:1".format(search, search)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=ret_))
        elif len(cond) == 2:
            num = int(cond[1])
            if num <= len(data["result"]):
                music = data["result"][num - 1]
                source = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(music["sid"]))
                data = source.text
                data = json.loads(data)
                if data["result"] != []:
                    ret_ = "[ RESULT ]"
                    ret_ += "\n\n~ Judul : {}".format(data["result"]["song"])
                    ret_ += "\n~ Album : {}".format(data["result"]["album"])
                    ret_ += "\n~ Ukuran : {}".format(data["result"]["size"])
                    ret_ += "\n~ Link : {}".format(data["result"]["mp3"][0])
                    ret_ += "\n\n[ FINISH ]"
                    image_message = ImageSendMessage(
                        original_content_url=data["result"]["img"],
                        preview_image_url=data["result"]["img"]
                    )

                    line_bot_api.reply_message(
                        event.reply_token,
                        image_message
                    )
                    return
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=ret_))
                    audio_message = AudioSendMessage(
                        original_content_url=data["result"]["mp3"][0],
                        duration=data["result"]["mp3"][0]
                    )

                    line_bot_api.reply_message(
                        event.reply_token,
                        audio_message
                    )
                    return


    elif '.carivideo ' in text:
        query = text.replace(".carivideo ","")
        with requests.session() as s:
            s.headers['user-agent'] = 'Mozilla/5.0'
            url = 'http://www.youtube.com/results'
            params = {'search_query': query}
            source = s.get(url, params=params)
            bsoup = BeautifulSoup(source.content, 'html5lib')
            num = 0
            hasil = "[ SEARCH RESULT ]\n\n"
            for a in bsoup.select('.yt-lockup-title > a[title]'):
                num += 1
                if '&list=' not in a['href']:
                    judul = "{}. Judul: ".format(num)
                    hasil += judul + ''.join((a['title'],'\n    Link : https://www.youtube.com' + a['href'],'\n\n'))
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=hasil))


    elif ".tr-" in text:
        separate = text.split("-")
        separate = separate[1].split(" ")
        lang = separate[0]
        say = text.replace(".tr-" + lang + " ","")
        if lang not in list_language["list_translate"]:
            return line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bahasa tujuan translate tidak ditemukan."))
        translator = Translator()
        hasil = translator.translate(say, dest=lang)
        tr = hasil.text
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="[ RESULT ]\n~ Translate ke bahasa: " + list_language["list_translate"] + "\n\n" + tr + "\n\n[ FINISH ]))



if __name__ == "__main__":
    app.run()
