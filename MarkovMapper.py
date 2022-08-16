import json
import random
import Utils
from Utils import noteJSON as nJ
from Utils import generateCutPath as cP
from Utils import generateTimesAndPlacements as tP
from Utils import noteDict as nD


noteDict = nD
sums = json.load(open('sums.txt', 'r'))
FIRST_RIGHT_NOTE = '2110'
FIRST_LEFT_NOTE = '1100'
START_BEAT = 4
noteTimes, notePlacements = tP('look.dat')
# work off probabilities
def mapDifficulty(songFolderName, difficulty, style, numBeats=200):
    dat = open(songFolderName+'\\'+difficulty+style+'.dat', 'r')
    datJSON = json.load(dat)
    dat.close()
    dat = open(songFolderName+'\\'+difficulty+style+'.dat', 'w')
    datJSON['_notes'] = []
    lastNotes = {
        '0': FIRST_LEFT_NOTE,
        '1': FIRST_RIGHT_NOTE,
        '-1': FIRST_LEFT_NOTE
    }

    for nt in noteTimes:
        placingRightNote, placingLeftNote = determinePlacingNotes(nt, noteTimes)
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
    # Dump new notes json into difficulty.dat
    json.dump(datJSON, dat)


def generateNote(prevNote, prevHandedNote):
    while True:
        # nextNote = noteDict[prevHandedNote][random.randint(0, len(noteDict[prevHandedNote]) - 1)]
        nextNote = None
        n = random.randint(1, sums[prevHandedNote])
        sum = 0
        for note, freq in noteDict[prevHandedNote]:
            if sum + 1 <= n <= sum + freq:
                nextNote = note
                break
            sum += freq

        if nextNote is None:
            raise Exception("bad random formula")

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
    # same coordinate is a vision block
    return prevNote[0] == currNote[0]


def isOppositeColumn(prevNote, currNote):
    if prevNote[2] == currNote[2]:
        return False
    prevOC = int(prevNote[0], 16) % 4 not in [3 * int(prevNote[2]), 2, 1]
    currOC = int(currNote[0], 16) % 4 not in [3 * int(currNote[2]), 2, 1]
    if prevOC and currOC:
        return True
    return False


def determinePlacingNotes(time, times):
    i = times.index(time)
    return notePlacements[i]
    # if notes are too close together it will only place one of the two notes
    # if times[i-1] >= time - 0.25 and times[i+1] <= time + 0.25:
    #     return [(True, False), (False, True)][random.randint(0, 1)]
    # else:
    #     return [(True, False), (False, True), (True, True)][random.randint(0, 2)]
        