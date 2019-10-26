import json


def get_timetable(postback):
    f = open('json/ele.json')
    jsn = json.load(f)
    f.close()
    text = ''
    count = 1
    for subject in jsn[str(day)].items():
        text += '【' + subject[0] + '時間目】\n' + subject[1] + '\n'
        if count == len(jsn[str(day)]):
            text += '\n' + subject[0][-1] + '時間授業です。'
        count += 1
    return text