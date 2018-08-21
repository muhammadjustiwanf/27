import requests, random
from bs4 import BeautifulSoup

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('HjEZRNk3czUVKof7ZLxIO3Bv8zdkeW1UBTPl9HNMmYgVHtQapRJr2ZyVB8qOMVrdmkTDfZ7nRjnavXF8xgO9qeBVd47MSgfP3k0J+oPWjw8+8dli+crm5VKHcFi+xidY2razYmls+0EC9CxIYnbOYwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a4ce4df86f3b49ce0ab0a91f1f4fec16')


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


def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    res = requests.get(target_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 10:
            return content

        heading = data.select_one('h1').text
        link = data['href']

        content += "{}\n{}\n\n".format(heading, link)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'Apple news':
        content = apple_news()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content)
    )


if __name__ == "__main__":
    app.run()
