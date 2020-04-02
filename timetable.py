# import json
import app
# from flask_sqlalchemy import SQLAlchemy


# def get_timetable(postback):
#     file_path = 'json/' + postback[0] + '/' + postback[1:-3] + '.json'
#     f = open(file_path)
#     jsn = json.load(f)
#     f.close()
#     count = 1
#     day_list = {'Mon': '月曜日', 'Tue': '火曜日', 'Wed': '水曜日', 'Thu': '木曜日', 'Fri': '金曜日'}
#     day = postback[-3:]
#     text = day_list[day] + 'の時間割です。\n\n'
#     for subject in jsn[day].items():
#         text += '【' + subject[0] + '時間目】\n' + subject[1] + '\n\n'
#         if count == len(jsn[day]):
#             text += '\n' + subject[0][-1] + '時間授業です。'
#         count += 1
#     return text


def get_timetable(postback):
    day_list = {'Mon': '月曜日', 'Tue': '火曜日', 'Wed': '水曜日', 'Thu': '木曜日', 'Fri': '金曜日'}
    timetables = app.Timetable.query.filter_by(
        grade=postback[0],
        course=postback[1:-3],
        day=postback[-3:]).order_by(app.Timetable.time).all()
    text = day_list[postback[-3:]] + 'の時間割です。\n\n'
    for timetable in timetables:
        text += '【' + str(timetable.time) + '時間目】\n' + timetable.subject + '\n\n'
    text += '\n' + str(timetables[-1].time) + '時間授業です。'
    return text
