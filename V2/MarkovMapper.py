import json


def noteAsJSON(name, time):
    data = {
        "_time": time,
        "_lineIndex": int(name[0], 16) % 4,
        "_lineLayer": int(name[0], 16)//4,
        "_type": int(name[2]),
        "_cutDirection": int(name[1])
    }
    return data


def generateMap():
    diff_dict = {
        '_version': '2.0.0',
        # '_customData': {

        # }
        '_notes': [],
        '_events': []
    }

    with open('generation.txt', 'r') as f:
        frames = f.readlines()
    
    for i in range(len(frames)):
        frame_notes = frames[i].split(' ')
        for n in frame_notes[:-1]:
            diff_dict['_notes'].append(noteAsJSON(n, i + 5))

    with open('export\\ExpertPlusStandard.dat', 'w') as f:
        json.dump(diff_dict, f)


generateMap()