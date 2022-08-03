import json
import random
import Utils
from Utils import noteJSON as nJ
from Utils import generateCutPath as cP
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
    placingLeftNote = random.randint(0, 1) == 1
    placingRightNote = random.randint(0, 1) == 1

    noteTimes = [x/2 + START_BEAT for x in range(1, 400)]  # Temporary placeholder value

    for nt in noteTimes:
        if placingRightNote and placingLeftNote:
            dominance = random.randint(0, 1)
            while True:
                note1 = generateNote(lastNotes['-1'], lastNotes[str(dominance)])
                note2 = generateNote(note1, lastNotes[str(dominance ^ 1)])
                if not isBadDouble(note1, note2):
                    break
            lastNotes[str(dominance)] = note1
            lastNotes[str(dominance ^ 1)] = note2
            datJSON['_notes'].append(nJ(note1, nt))
            datJSON['_notes'].append(nJ(note2, nt))
            lastNotes['-1'] = note2
        elif placingRightNote:
            nextRightNote = generateNote(lastNotes['-1'], lastNotes['1'])
            datJSON['_notes'].append(nJ(nextRightNote, nt))
            lastNotes['1'] = nextRightNote
            lastNotes['-1'] = nextRightNote
        elif placingLeftNote:
            nextLeftNote = generateNote(lastNotes['-1'], lastNotes['0'])
            datJSON['_notes'].append(nJ(nextLeftNote, nt))
            lastNotes['0'] = nextLeftNote
            lastNotes['-1'] = nextLeftNote
        placingRightNote = random.randint(0, 1) == 1
        placingLeftNote = random.randint(0, 1) == 1
    # Dump new notes json into difficulty.dat
    json.dump(datJSON, dat)


def generateNote(prevNote, prevHandedNote):
    while True:
        nextNote = noteDict[prevHandedNote][random.randint(0, len(noteDict[prevHandedNote]) - 1)]
        if not isBadNote(prevNote, nextNote):
            break
    return nextNote


def isBadDouble(note1, note2):
    if note2[0] in cP(note1) or note1[0] in cP(note2):
        return True
    return False


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
