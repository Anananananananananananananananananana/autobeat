import json
import random
import Utils
from Utils import noteJSON as nJ
noteDict = Utils.noteDict

FIRST_RIGHT_NOTE = '2110'
FIRST_LEFT_NOTE = '9001'
START_BEAT = 4



def mapDifficulty(songFolderName, difficulty, style, numBeats=200):
    dat = open(songFolderName+'\\'+difficulty+style+'.dat', 'r')
    datJSON = json.load(dat)
    dat.close()
    dat = open(songFolderName+'\\'+difficulty+style+'.dat', 'w')
    datJSON['_notes'] = [nJ(FIRST_RIGHT_NOTE, START_BEAT), nJ(FIRST_LEFT_NOTE, START_BEAT)]
    lastNotes = {
        '0': FIRST_LEFT_NOTE,
        '1': FIRST_RIGHT_NOTE,
        '-1': FIRST_LEFT_NOTE
    }
    placingLeftNote = True
    placingRightNote = True


    noteTimes = range(START_BEAT + 1, numBeats + START_BEAT)   # Temporary placeholder value
    print(noteTimes)

    for nt in noteTimes:
        if placingRightNote:
            while True:
                nextRightNote = noteDict[lastNotes['1']][random.randint(0, len(noteDict[lastNotes['1']]) - 1)]
                if not isBadNote(lastNotes['-1'], nextRightNote):
                    break
                print(nextRightNote)
            datJSON['_notes'].append(nJ(nextRightNote, nt))
            lastNotes['1'] = nextRightNote
            lastNotes['-1'] = nextRightNote
        if placingLeftNote:
            while True:
                nextLeftNote = noteDict[lastNotes['0']][random.randint(0, len(noteDict[lastNotes['0']])-1)]
                if not isBadNote(lastNotes['-1'], nextLeftNote):
                    break
                print(nextLeftNote,lastNotes['-1'], lastNotes['0'])
            datJSON['_notes'].append(nJ(nextLeftNote, nt))
            lastNotes['0'] = nextLeftNote
            lastNotes['-1'] = nextLeftNote
        

    # Dump new notes json into difficulty.dat
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
