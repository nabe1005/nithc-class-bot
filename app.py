import os
import affiliation
import richmenu
import timetable


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'affiliation':
        line_bot_api.reply_message(event.reply_token, affiliation.get_grade)
    elif event.postback.data.startswith('grade='):
        affiliation.set_grade(event.postback.data)
        line_bot_api.reply_message(event.reply_token, affiliation.get_course())
    elif event.postback.data.startswith('course='):
        affiliation.set_course(event.postback.data, event.source.user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(event.postback.data)))
    elif event.postback.data in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=timetable.get_timetable(event.postback.data)))
    else:
        richmenu.unlink(event.source.user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(event.postback.data)))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
