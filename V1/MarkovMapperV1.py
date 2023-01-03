import json
import random
from UtilsV1 import noteJSON
from UtilsV1 import generateCutPath
from UtilsV1 import generateTimesAndPlacements
noteDict = json.load(open('good.txt', 'r'))


sums = json.load(open('sums.txt', 'r'))
FIRST_RIGHT_NOTE = '7311'
FIRST_LEFT_NOTE = '8401'
START_BEAT = 4
noteTimes, notePlacements = generateTimesAndPlacements('look.dat')


# Generates the notes sequentially and places them in a dat file that Beat Saber can understand
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
        placingLeftNote, placingRightNote = determinePlacingNotes(nt, noteTimes)
        if placingRightNote and placingLeftNote:
            dominance = random.randint(0, 1)
            while True:
                note1 = generateNote(lastNotes['-1'], lastNotes[str(dominance)])
                note2 = generateNote(note1, lastNotes[str(dominance ^ 1)])
                if not isBadDouble(note1, note2):
                    break
            lastNotes[str(dominance)] = note1
            lastNotes[str(dominance ^ 1)] = note2
            datJSON['_notes'].append(noteJSON(note1, nt))
            datJSON['_notes'].append(noteJSON(note2, nt))
            lastNotes['-1'] = note2
        elif placingRightNote:
            nextRightNote = generateNote(lastNotes['-1'], lastNotes['1'])
            datJSON['_notes'].append(noteJSON(nextRightNote, nt))
            lastNotes['1'] = nextRightNote
            lastNotes['-1'] = nextRightNote
        elif placingLeftNote:
            nextLeftNote = generateNote(lastNotes['-1'], lastNotes['0'])
            datJSON['_notes'].append(noteJSON(nextLeftNote, nt))
            lastNotes['0'] = nextLeftNote
            lastNotes['-1'] = nextLeftNote
    # Dump new notes json into difficulty.dat
    json.dump(datJSON, dat)


# generates the next note based on the last note placed,
# and the last note of the same hand placed (Which may be the same)
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


# does a loose check to see if a "double" is humanly impossible to hit
def isBadDouble(note1, note2):
    if note2[0] in generateCutPath(note1) or note1[0] in generateCutPath(note2):
        return True
    return False


# does a loose check to see if a note meets the criteria to place in the map
def isBadNote(prevNote, currNote):
    return isVisionBlock(prevNote, currNote) or isOppositeColumn(prevNote, currNote)


# does a loose check to seee if this note is blocked by a previously placed note
def isVisionBlock(prevNote, currNote):
    # same coordinate is a vision block
    return prevNote[0] == currNote[0] and prevNote[2] != currNote[2]


def isOppositeColumn(prevNote, currNote):
    if prevNote[2] == currNote[2]:
        return False
    prevOC = int(prevNote[0], 16) % 4 not in [3 * int(prevNote[2]), 2, 1]
    currOC = int(currNote[0], 16) % 4 not in [3 * int(currNote[2]), 2, 1]
    if prevOC and currOC:
        return True
    return False


# determines which note to place
def determinePlacingNotes(time, times):
    i = times.index(time)
    return notePlacements[i]
    # if notes are too close together it will only place one of the two notes
    # if times[i-1] >= time - 0.25 and times[i+1] <= time + 0.25:
    #     return [(True, False), (False, True)][random.randint(0, 1)]
    # else:
    #     return [(True, False), (False, True), (True, True)][random.randint(0, 2)]
