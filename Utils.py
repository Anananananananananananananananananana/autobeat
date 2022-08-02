




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

