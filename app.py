import os

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

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ[
    'z9U8Vuu7SIUmd27ZoWmMckOoWuK+38JXJ5DZcVx3Akm+VyjflwRv0AsCQ+JhGW31dsWb1Sxf47O0XUHoKu/H6xhktF3fCc+8RVg3/z9L6OqJj8OsP9BF3YVqFAVc90sKrGcMLjiP2yyENhLBpv/02gdB04t89/1O/w1cDnyilFU=']
YOUR_CHANNEL_SECRET = os.environ['83b0f0d2498dd9a9084e944b97aaa069']

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@app.route('/', methods=['POST'])
def index():
    return 'OK!'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
