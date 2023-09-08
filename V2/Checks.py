def isDD(prevHandedNoteJSON, noteJSON):
    return prevHandedNoteJSON["_cutDirection"] == noteJSON["_cutDirection"]


def isInline(prevNoteJSON, noteJSON):
    return prevNoteJSON["_type"] != noteJSON["_type"] and prevNoteJSON["_lineIndex"] == noteJSON["_lineIndex"] \
        and prevNoteJSON["_lineLayer"] == noteJSON["_lineLayer"]


def isInOppositeColumn(note1JSON, note2JSON):
    return note1JSON["_type"] != note2JSON["_type"] and note1JSON["_lineIndex"] == 3 * (3-note1JSON["_type"]) \
        and note2JSON["_lineIndex"] == 3 * (3-note2JSON["_type"])


def inImmediateCutPath(note1JSON, note2JSON):
    cutPaths = [[(0, 1)],
                [(0, -1)],
                [(-1, 0)],
                [(1, 0)],
                [(0, 1), (-1, 0), (1, -1)],
                [(0, 1), (1, 0), (1, 1)],
                [(0, -1), (1, 0), (1, -1)],
                [(0, -1), (-1, 0), (-1, -1)],
                []]
    for index, layer in cutPaths[note1JSON["_cutDirection"]]:
        if note2JSON["_lineIndex"] == note1JSON["_lineIndex"]+index \
                and note2JSON["_lineLayer"] == note1JSON["_lineLayer"]+layer:
            return True
    for index, layer in cutPaths[note2JSON["_cutDirection"]]:
        if note1JSON["_lineIndex"] == note2JSON["_lineIndex"]+index \
                and note1JSON["_lineLayer"] == note2JSON["_lineLayer"]+layer:
            return True
    return False


def isWindow(note1JSON, note2JSON):
    cutPaths = [[(0, 2)],
                [(0, -2)],
                [(-2, 0)],
                [(2, 0)],
                [(-1, 2), (-2, 1), (2, -2)],
                [(1, 2), (2, 1), (2, 2)],
                [(1, -2), (2, 1), (2, -2)],
                [(1, -2), (-2, 1), (-2, -2)],
                []]
    for index, layer in cutPaths[note1JSON["_cutDirection"]]:
        if note2JSON["_lineIndex"] == note1JSON["_lineIndex"]+index \
                and note2JSON["_lineLayer"] == note1JSON["_lineLayer"]+layer:
            return True
    for index, layer in cutPaths[note2JSON["_cutDirection"]]:
        if note1JSON["_lineIndex"] == note2JSON["_lineIndex"]+index \
                and note1JSON["_lineLayer"] == note2JSON["_lineLayer"]+layer:
            return True
    return False


def isStack(note1JSON, note2JSON):
    return note1JSON["_type"] == note2JSON["_type"] and note1JSON["_cutDirection"] == note2JSON["_cutDirection"] \
        and inImmediateCutPath(note1JSON, note2JSON)