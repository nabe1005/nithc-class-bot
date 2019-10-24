import datetime
import os
import json

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate, PostbackAction, URIAction, MessageAction, ConfirmTemplate,
    DatetimePickerAction, QuickReply, QuickReplyButton)
from dotenv import load_dotenv

app = Flask(__name__)
app.debug = False

load_dotenv(verbose=True)
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
channel_secret = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


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


@app.route('/', methods=['GET'])
def index():
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '時間割':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='何曜日の時間割ですか？',
                quick_reply=QuickReply(items=[
                    QuickReplyButton(action=PostbackAction(label='月', data='Mon', display_text='月曜日')),
                    QuickReplyButton(action=PostbackAction(label='火', data='Tue', display_text='火曜日')),
                    QuickReplyButton(action=PostbackAction(label='水', data='Tue', display_text='水曜日')),
                    QuickReplyButton(action=PostbackAction(label='木', data='Tue', display_text='木曜日')),
                    QuickReplyButton(action=PostbackAction(label='金', data='Tue', display_text='金曜日'))
                ])
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='エラー')
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    f = open('json/kairoele.json')
    jsn = json.load(f)
    f.close()
    timetable = json.dumps(jsn[str(event.postback.data)], sort_keys=True, indent=4)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(timetable))
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
