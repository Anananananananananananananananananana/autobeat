import json
import random
import Utils
from Utils import noteJSON as nJ
noteDict = Utils.noteDict


def mapDifficulty(songFolderName, difficulty, style, numNotes=200):
    dat = open(songFolderName+'\\'+difficulty+style+'.dat', 'r')
    datJSON = json.load(dat)
    dat.close()
    dat = open(songFolderName+'\\'+difficulty+style+'.dat', 'w')
    datJSON['_notes'] = ['2110', '9001']
    lastNotes = {
        '0': '9001',
        '1': '2110'
    }
    placingLeftNote = True
    placingRightNote = True
    for i in range(numNotes):
        if placingRightNote:
            while True:
                nextRightNote = noteDict[lastNotes['1']][random.randint(0, len(noteDict[lastNotes['1']]) - 1)]
                if not isBadNote(datJSON['_notes'][-1], nextRightNote):
                    break
            datJSON['_notes'].append(nextRightNote)
            lastNotes['1'] = nextRightNote
        if placingLeftNote:
            while True:
                nextLeftNote = noteDict[lastNotes['0']][random.randint(0, len(noteDict[lastNotes['0']])-1)]
                if not isBadNote(datJSON['_notes'][-1], nextLeftNote):
                    break
            datJSON['_notes'].append(nextLeftNote)
            lastNotes['0'] = nextLeftNote
    for time in range(len(datJSON['_notes'])):
        datJSON['_notes'][time] = nJ(datJSON['_notes'][time], time)
    json.dump(datJSON, dat)


def isBadNote(prevNote, currNote):
    return isVisionBlock(prevNote, currNote) or isOppositeColumn(prevNote, currNote)


def isVisionBlock(prevNote, currNote):
    # opposite hands, same coordinate is a vision block
    return prevNote[0] == currNote[0] and prevNote[2] != currNote[2]


def isOppositeColumn(prevNote, currNote):
    if prevNote[2] == currNote[2]:
        return False
    prevOC = int(prevNote[0], 16) % 4 not in [3 * int(prevNote[2]), 2, 1]
    currOC = int(currNote[0], 16) % 4 not in [3 * int(currNote[2]), 2, 1]
    if prevOC and currOC:
        return True
    return False
