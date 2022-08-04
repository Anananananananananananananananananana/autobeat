import json


def mirrorNote(note_ID):
    new_coord = hex(int(note_ID[0], 16) ^ 0b11)
    if note_ID[1] in ['4', '2', '6']:
        new_cut = str(int(note_ID[1]) + 1)
    elif note_ID[1] in ['5','3','7']:
        new_cut = str(int(note_ID[1]) - 1)
    else:
        new_cut = note_ID[1]
    new_hand = str(int(note_ID[2]) ^ 1)

    return (new_coord + new_cut + new_hand + note_ID[3])[2:]


def mirrorNoteDict(dict):
    new_dict = {}
    for key in dict:
        note_list = [mirrorNote(k) for k in dict[key]]
        new_dict.update({mirrorNote(key): note_list})
    return new_dict


def noteJSON(noteName, time):
    data = {
        "_time": time,
        "_lineIndex": int(noteName[0], 16) % 4,
        "_lineLayer": int(noteName[0], 16)//4,
        "_type": int(noteName[2]),
        "_cutDirection": int(noteName[1])
    }
    return data


def noteCSVtoDict(csv):
    noteDict = dict()
    vals = open(csv, 'r')
    for line in vals.readlines():
        chains = line[:-1].split(',')
        noteDict[chains[0]] = [c for c in chains[1:] if c != '']
    return noteDict


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


noteDict = noteCSVtoDict('RightHand.csv')
noteDict.update(mirrorNoteDict(noteDict))
