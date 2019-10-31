from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import scraping

app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# シス創のホームページ
URL = "http://www.si.t.u-tokyo.ac.jp/"

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
    if event.reply_token == "00000000000000000000000000000000":
        return


    soup=scraping.load_site(URL)
    notic_list=scraping.find_by_id(soup,"notic_list")
    notic_students_list=scraping.find_by_id(soup,"notic_students_list")

    notic_message=notic_list[0]["string"]
    notic_students_message=notic_students_list[0]["string"]

    if(event.message.text=="学科からのお知らせ"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=notic_students_message))

    if(event.message.text=="学科生の方へのお知らせ"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=notic_students_message))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)