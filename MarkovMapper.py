import json
import random

noteDict = {
    'b511': ['1610', '2110'],
    '1610': ['b511', '7511'],
    '2110': ['b511', '7511'],
    '7511': ['1610', '2110']
}


def mapDifficulty(songFolderName, style, difficulty, numNotes=20):
    dat = open(songFolderName+'\\'+difficulty+style+'.dat', 'r')
    datJSON = json.load(dat)
    dat.close()
    dat = open(songFolderName+'\\'+difficulty+style+'.dat', 'w')
    datJSON['_notes'] = ['2110']
    for i in range(numNotes):
        length = len(noteDict[datJSON['_notes'][i]])
        datJSON['_notes'].append(noteDict[datJSON['_notes'][i]][random.randint(0, length-1)])
    for time in range(len(datJSON['_notes'])):
        datJSON['_notes'][time] = noteJSON(datJSON['_notes'][time], time)
    json.dump(datJSON, dat)


def noteJSON(noteName, time):
    data = {
        "_time" : time,
        "_lineIndex": int(noteName[0], 16) % 4,
        "_lineLayer": int(noteName[0], 16)//4,
        "_type": int(noteName[2]),
        "_cutDirection": int(noteName[1])
    }
    return data


mapDifficulty('test', 'Standard', 'ExpertPlus')
