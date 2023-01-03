from FileGenerator import mkFiles

# To be user inputted
songInfo = {
    'name': 'SONGNAME',
    'subName': '',
    'artist': 'ARTIST',
    'bpm': 128,
    'cover': ''
}

mapInfo = {
    'pStart': 1,
    'pDur': 10,
    'env': 'DefaultEnvironment',
}

eplusInfo = {
        'type': 'Standard',
        'diff': 'ExpertPlus',
        'njs': 20,
        'offset': .067
}

easyInfo = {
        'type': 'Standard',
        'diff': 'Easy',
        'njs': 16,
        'offset': .067
}

# difficulties should be sorted from Easy to ExpertPlus
difficulties = [easyInfo, eplusInfo]

mkFiles('look.ogg', songInfo, mapInfo, difficulties)

