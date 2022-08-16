import json

noteDict = json.load(open('good.txt', 'r'))
SLIDER_TIMING = 1/13

def noteJSON(name, time):
    data = {
        "_time": time,
        "_lineIndex": int(name[0], 16) % 4,
        "_lineLayer": int(name[0], 16)//4,
        "_type": int(name[2]),
        "_cutDirection": int(name[1])
    }
    return data


def noteName(JSON, parity=''):
    coord = [['8', '9', 'a', 'b'],
             ['4', '5', '6', '7'],
             ['0', '1', '2', '3']]
    return coord[2-JSON['_lineLayer']][JSON['_lineIndex']]+str(JSON['_cutDirection'])+str(JSON['_type'])+str(parity)


def generateCutPath(noteName):
    cutPaths = {
        '0': lambda k: [k - 4],
        '1': lambda k: [k + 4],
        '2': lambda k: [k + 1],
        '3': lambda k: [k - 1],
        '4': lambda k: [k + 1, k - 4, k - 3],
        '5': lambda k: [k - 1, k - 4, k - 5],
        '6': lambda k: [k + 1, k + 4, k + 5],
        '7': lambda k: [k - 1, k + 4, k + 3]
    }
    coord = int(noteName[0], 16)
    cut = noteName[1]
    unfiltered = cutPaths[cut](coord)
    filtered = []
    for c in unfiltered:
        if not 0 <= c <= 11:
            continue
        elif {c, coord} in [{0, 3}, {3, 4}, {4, 7}, {7, 8}, {8, 11}]:
            continue
        filtered.append(hex(c)[2:])
    return filtered


def generateNoteTimesFromDat(filepath):
    dat = json.load(open(filepath, 'r'))
    noteSet = set()
    noteTimes = []
    for note in dat['_notes']:
        if note['_type'] != 3:
            noteSet.add(note['_time'])
        if len(noteSet) > len(noteTimes):
            noteTimes.append(note['_time'])
    return noteTimes

def generateTimesAndPlacements(filepath):
    dat = json.load(open(filepath, 'r'))
    noteTimes = []
    notePlacements = []
    placing = [False, False]
    for note in dat['_notes']:
        if note['_type'] != 3:
            if len(noteTimes) == 0:
                noteTimes.append(note['_time'])
                placing[note['_type']] = True
            elif noteTimes[-1] == note['_time']:
                placing[note['_type']] = True
            elif noteTimes[-1] != note['_time']:
                notePlacements.append(placing)
                placing = [False, False]
                if noteTimes[-1] + SLIDER_TIMING < note['_time']:
                    placing[note['_type']] = True
                    noteTimes.append(note['_time'])
    notePlacements.append(placing)
    return noteTimes, notePlacements