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
    MessageEvent, PostbackEvent, TextMessage, TextSendMessage, FollowEvent
)
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
    richmenu.unlink(event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

# todo 授業変更に対応する。
@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'affiliation':
        line_bot_api.reply_message(event.reply_token, affiliation.get_grade)
    elif event.postback.data.startswith('grade='):
        affiliation.set_grade(event.postback.data)
        line_bot_api.reply_message(event.reply_token, affiliation.get_course())
    elif event.postback.data.startswith('course='):
        affiliation.set_course(event.postback.data, event.source.user_id)
        if event.postback.data.endswith('5'):
            line_bot_api.reply_message(event.reply_token, affiliation.confirm_gm(event.postback.data))
        else:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=str(affiliation.grade + affiliation.course)))
    elif event.postback.data.endswith(('Mon', 'Tue', 'Wed'))\
            or event.postback.data.endswith(('Thu', 'Fri')):
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=timetable.get_timetable(event.postback.data)))


@handler.add(FollowEvent)
def handle_follow(event):
    richmenu.unlink(str(event.source.user_id))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
