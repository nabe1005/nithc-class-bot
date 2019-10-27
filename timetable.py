import json


def get_timetable(postback):
    file_path = 'json/' + postback[0] + '/' + postback[1:-3] + '.json'
    f = open(file_path)
    jsn = json.load(f)
    f.close()
    text = ''
    count = 1
    day = postback[-3:]
    for subject in jsn[day].items():
        text += '【' + subject[0] + '時間目】\n' + subject[1] + '\n'
        if count == len(jsn[day]):
            text += '\n' + subject[0][-1] + '時間授業です。'
        count += 1
    return text
