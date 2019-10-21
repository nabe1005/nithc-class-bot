import datetime
import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, DatetimePickerTemplateAction,
    TemplateSendMessage, ButtonsTemplate, PostbackAction, URIAction, MessageAction, ConfirmTemplate)
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
            TemplateSendMessage(
                alt_text='Confirm template',
                template=ConfirmTemplate(
                    text='testだよ',
                    actions=[
                        MessageAction(
                            label='Yes',
                            text='yes'
                        ),
                        MessageAction(
                            label='No',
                            text='no'
                        )
                    ]
                )
            )
        )
    elif event.message.text == 'yes':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='yes')
        )
    elif event.message.text == 'no':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='no')
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='エラー')
        )


def send_text():
    day = ['月', '火', '水', '木', '金', '土', '日']
    num_day = datetime.date.today().weekday()
    return_day = day[num_day]
    return return_day


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
