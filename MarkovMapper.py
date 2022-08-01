import json
import random

noteDict = {
    'b501': ['1600', '2100'],
    '1600': ['b501', '7501'],
    '2100': ['b501', '7501'],
    '7501': ['1600', '2100']
}


def mapDifficulty(style, difficulty, numNotes=20):
    dat = open(difficulty+style+'.dat', 'r')
    datJSON = json.load(dat.read())
    datJSON['_events'] = ['2100']
    for i in range(numNotes):
        length = len(noteDict[datJSON['_events'][i]])
        datJSON['_events'].append(noteDict[datJSON['_events'][i]][random.randint(0, length-1)])
    for time in range(len(noteDict)):
        datJSON['_events'][time] = noteJSON(datJSON['_events'][time], time)
    dat.write(json.dump(datJSON))


def noteJSON(noteName, time):
    data = {
        "_time" : time,
        "_lineIndex": int(noteName[0], 16) % 4,
        "_lineLayer": int(noteName[0], 16)//4,
        "_type": int(noteName[2]),
        "_cutDirection": int(noteName[1])
    }
    return data

