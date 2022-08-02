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
        "_time": (time - (int(noteName[2]) ^ 1))/2 + 2,
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

noteDict = noteCSVtoDict('RightHand.csv')
noteDict.update(mirrorNoteDict(noteDict))

