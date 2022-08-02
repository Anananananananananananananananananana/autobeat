


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




noteDict = {
    'b511': ['1610', '2110', '4210', '9210'],
    '1610': ['b511', '7511', '7311', 'a511', 'a011'],
    '2110': ['b511', '7511', 'a511', 'a011'],
    '7511': ['1610', '2110', '4210', '9210'],
    '4210': ['b511', '7511', 'a511', '7311'],
    '9210': ['b511', '7511', '7311'],
    'a511': ['1610', '4210', '2110'],
    '7311': ['1610', '4210', '9210'],
    'a011': ['3710', '1610', '2110'],
    '3710': ['a011', 'b511']
}

noteDict.update(mirrorNoteDict(noteDict))

