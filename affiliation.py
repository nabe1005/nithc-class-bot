import richmenu
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, PostbackAction

grade = ''
course = ''

get_grade = TextSendMessage(
    text='学年を選択してください。',
    quick_reply=QuickReply(items=[
        QuickReplyButton(action=PostbackAction(label='1', data='grade=1', display_text='1年生')),
        QuickReplyButton(action=PostbackAction(label='2', data='grade=2', display_text='2年生')),
        QuickReplyButton(action=PostbackAction(label='3', data='grade=3', display_text='3年生')),
        QuickReplyButton(action=PostbackAction(label='4', data='grade=4', display_text='4年生')),
        QuickReplyButton(action=PostbackAction(label='5', data='grade=5', display_text='5年生'))
    ])
)


def get_course():
    if grade == '1':
        return TextSendMessage(
            text='クラスを選択してください',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=PostbackAction(label='1', data='course=1', display_text='1組')),
                QuickReplyButton(action=PostbackAction(label='2', data='course=2', display_text='2組')),
                QuickReplyButton(action=PostbackAction(label='3', data='course=3', display_text='3組')),
                QuickReplyButton(action=PostbackAction(label='4', data='course=4', display_text='4組')),
                QuickReplyButton(action=PostbackAction(label='5', data='course=5', display_text='5組'))
            ])
        )
    elif grade in ['2', '3']:
        return TextSendMessage(
            text='学科を選択してください',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=PostbackAction(label='機械', data='course=m', display_text='生産ー機械')),
                QuickReplyButton(action=PostbackAction(label='電気', data='course=e', display_text='生産ー電気')),
                QuickReplyButton(action=PostbackAction(label='情報', data='course=j', display_text='生産ー情報')),
                QuickReplyButton(action=PostbackAction(label='物質', data='course=c', display_text='物質環境')),
                QuickReplyButton(action=PostbackAction(label='社基', data='course=z', display_text='社会基盤')),
            ])
        )
    else:
        return TextSendMessage(
            text='履修コースを選択してください',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=PostbackAction(label='設計加工', data='course=des', display_text='設計加工')),
                QuickReplyButton(action=PostbackAction(label='エネルギー', data='course=ene', display_text='エネルギー')),
                QuickReplyButton(action=PostbackAction(label='回路エレ', data='course=ele', display_text='回路エレクトロニクス')),
                QuickReplyButton(action=PostbackAction(label='ITS', data='course=its', display_text='ITS')),
                QuickReplyButton(action=PostbackAction(label='ロボティクス', data='course=rob', display_text='ロボティクス')),
                QuickReplyButton(action=PostbackAction(label='GM', data='course=gm', display_text='GM')),
                QuickReplyButton(action=PostbackAction(label='材料物性', data='course=mat', display_text='材料物性')),
                QuickReplyButton(action=PostbackAction(label='バイオ環境', data='course=bio', display_text='バイオ環境')),
                QuickReplyButton(action=PostbackAction(label='都市デザイン', data='course=city', display_text='都市デザイン')),
                QuickReplyButton(action=PostbackAction(label='建築設計', data='course=con', display_text='建築設計'))
            ])
        )


def set_grade(data):
    global grade
    grade = data[-1]


def set_course(postback, user):
    global course
    course = postback[7:]
    richmenu.link_timetable_menu(grade, course, user)
