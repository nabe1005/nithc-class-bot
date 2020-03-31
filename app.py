import codecs
import os
import re
import time

import affiliation
import richmenu
import timetable


from flask import *

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
import json

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
def top():
    return 'OK'


@app.route('/register', methods=['GET'])
def form_timetable():
    f = open('json/class.json')
    jsn = json.load(f)
    f.close()
    f = open('subjects.txt')
    subjects = f.readlines()
    f.close()
    return render_template('register_timetable.html', classes=jsn, subjects=subjects)


@app.route('/register', methods=['POST'])
def register_timetable():
    day_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    sub = {'Mon': {}, 'Tue': {}, 'Wed': {}, 'Thu': {}, 'Fri': {}}
    for day in day_list:
        for i in range(1, 6):
            if request.form.get(day + str(i)):
                sub[day][i] = request.form.get(day + str(i)).replace('|', '\\')
    file_path = 'json/' + request.form.get('grade') + '/' + request.form.get('class') + '.json'
    with codecs.open(file_path, 'w', 'utf-8') as f:
        json.dump(sub, f, indent=2, ensure_ascii=False)
    return sub


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
        time.sleep(1)
        line_bot_api.reply_message(event.reply_token, affiliation.get_course())
    elif event.postback.data.startswith('course='):
        if event.postback.data.endswith('its'):
            if affiliation.gm_flag == 0:
                affiliation.gm_flag = 1
                time.sleep(1)
                line_bot_api.reply_message(event.reply_token, affiliation.confirm_gm(event.postback.data))
            else:
                affiliation.set_course(event.postback.data, event.source.user_id)
                time.sleep(1)
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(text=str(affiliation.grade + affiliation.course)))
        else:
            affiliation.set_course(event.postback.data, event.source.user_id)
            time.sleep(1)
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
