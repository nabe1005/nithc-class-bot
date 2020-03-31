import os

from linebot import LineBotApi
from dotenv import load_dotenv
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, PostbackAction

load_dotenv(verbose=True)
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
line_bot_api = LineBotApi(channel_access_token)


def all_clear():
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
        line_bot_api.delete_rich_menu(rich_menu_id=rich_menu.rich_menu_id)


def create_affiliation_menu():
    affiliation_menu = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=True,
        name='affiliation',
        chat_bar_text='学年・学科を設定',
        areas=[RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
            action=PostbackAction(
                label='affiliation',
                data='affiliation'
            )
        )]
    )

    affiliation_id = line_bot_api.create_rich_menu(rich_menu=affiliation_menu)

    with open('static/affiliation.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id=affiliation_id, content_type='image/png', content=f)

    line_bot_api.set_default_rich_menu(affiliation_id)


def create_timetable_menu():
    affiliations = {
        '11', '12', '13', '14', '15',
        '2m', '2e', '2j', '2c', '2z',
        '3m', '3e', '3j', '3c', '3z',
        '4m', '4e', '4j', '4c', '4z',
        '5des', '5ene', '5ele', '5rob', '5its',
        '5mat', '5bio', '5city', '5con','5gm',
    }

    for affiliation in affiliations:
        timetable_menu = RichMenu(
            size=RichMenuSize(width=2500, height=1686),
            selected=True,
            name='timetable' + affiliation,
            chat_bar_text='時間割を確認',
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=500, height=1000),
                    action=PostbackAction(label='Mon', data=str(affiliation + 'Mon'))
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=500, y=0, width=500, height=1000),
                    action=PostbackAction(label='Tue', data=str(affiliation + 'Tue'))
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1000, y=0, width=500, height=1000),
                    action=PostbackAction(label='Wed', data=str(affiliation + 'Wed'))
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1500, y=0, width=500, height=1000),
                    action=PostbackAction(label='Thu', data=str(affiliation + 'Thu'))
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=2000, y=0, width=500, height=1000),
                    action=PostbackAction(label='Fri', data=str(affiliation + 'Fri'))
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=1000, width=2500, height=686),
                    action=PostbackAction(label='affiliation', data='affiliation')
                ),
            ]
        )

        timetable_id = line_bot_api.create_rich_menu(rich_menu=timetable_menu)

        with open('static/timetable.png', 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id=timetable_id, content_type='image/png', content=f)


def unlink(user):
    line_bot_api.unlink_rich_menu_from_user(user_id=user)


def link_timetable_menu(grade, course, user):
    menu_list = line_bot_api.get_rich_menu_list()
    for menu in menu_list:
        if menu.name != 'timetable' + grade + course:
            continue
        line_bot_api.link_rich_menu_to_user(user_id=user, rich_menu_id=menu.rich_menu_id)
        break
