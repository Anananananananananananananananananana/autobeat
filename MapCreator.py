import json
import os

POSSIBLE_DIFF_NAMES = ['Easy', 'Normal', 'Hard', 'Expert', 'ExpertPlus']
DIFFICULTY_RANKS = {
    'Easy': 1,
    'Normal': 3,
    'Hard': 5,
    'Expert': 7,
    'ExpertPlus': 9
}


def createInfoDict(songInfo, mapInfo, customSongData=None):
    info = {
        '_version': '2.0.0',
        '_songName': songInfo['name'],
        '_songSubName': songInfo['subName'],
        '_songAuthorName': songInfo['artist'],
        '_levelAuthorName': 'AutoBeat',
        '_beatsPerMinute': songInfo['bpm'],
        '_shuffle': 0,
        '_shufflePeriod': 0.5,
        '_previewStartTime': mapInfo['pStart'],
        '_previewDuration': mapInfo['pDur'],
        '_songFilename': songInfo['audio'],
        '_coverImageFilename': songInfo['cover'],
        '_environmentName': mapInfo['env'],
        '_allDirectionsEnvironmentName': 'GlassDesertEnvironment',
        '_songTimeOffset': 0,
        '_difficultyBeatmapSets': []
    }
    if customSongData is not None:
        info['_customData'] = customSongData
    return info

def createDifficulty(songFolderName, diff, style):
    diff_dict = {
        '_version': '2.0.0',
        # '_customData': {

        # }
        '_events': []
    }
    f = open(songFolderName + '\\' + diff + style + '.dat', 'w')
    f.write(json.dump(diff_dict))
    f.close()


# updates an existing difficulty or creates a new one if specified difficulty does not exist
def updateDifficulty(info, diffInfo, customData=None):
    difficultyJSON = {
        "_difficulty": diffInfo['diff'],
        "_difficultyRank": DIFFICULTY_RANKS[diffInfo['diff']],
        "_beatmapFilename": diffInfo['diff'] + diffInfo['type'] + '.dat',
        "_noteJumpMovementSpeed": diffInfo['njs'],
        "_noteJumpStartBeatOffset": diffInfo['offset']
    }

    setJSON = {
        '_beatmapCharacteristicName': 'Standard',
        '_difficultyBeatmaps': []
    }

    if customData is not None:
        difficultyJSON['_customData'] = customData

    setIndex = len(info['_difficultyBeatmapSets'])
    for s in range(len(info['_difficultyBeatmapSets'])):
        if info['_difficultyBeatmapSets'][s]['_beatmapCharacteristicName'] == diffInfo['type']:
            setIndex = s
            break
    if setIndex == len(info['_difficultyBeatmapSets']):
        info['_difficultyBeatmapSets'].append(setJSON)

    for d in range(len(info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'])):
        if info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'][d]['_difficultyRank'] > DIFFICULTY_RANKS[diffInfo['diff']]:
            info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'].insert(d, difficultyJSON)
            return
        elif info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'][d]['_difficultyRank'] == DIFFICULTY_RANKS[diffInfo['diff']]:
            info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'][d] = difficultyJSON
            return
    info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'].append(difficultyJSON)


def createInfoDat(info, songFolderName):
    infoJSON = json.dumps(info, indent=2)
    f = open(songFolderName+'\\Info.dat', 'w')
    f.write(infoJSON)
    f.close()




def createSongFolder(songFolderName):
    if not os.path.exists(songFolderName):
        os.mkdir(songFolderName)


def createTestFolder():
    createSongFolder('test')
    songInfo = {
        'name': 'SLIME INCIDENT',
        'subName': '',
        'artist': 'Camellia',
        'bpm': 160,
        'audio': 'slime.egg',
        'cover': 'cover.jpg'
    }
    mapInfo = {
        'pStart': 200,
        'pDur': 10,
        'env': 'DefaultEnvironment',
    }
    infoDict = createInfoDict(songInfo, mapInfo)

    eInfo = {
        'type': 'Standard',
        'diff': 'Expert',
        'njs': 18,
        'offset': -0.4
    }
    eCustomData = {
        '_difficultyLabel': 'SMOOTH SCENARIO'
    }
    eplusInfo = {
        'type': 'Standard',
        'diff': 'ExpertPlus',
        'njs': 20,
        'offset': -0.725
    }

    eplusCustomData = {
        '_difficultyLabel': 'STICKY SITUATION'
    }
    updateDifficulty(infoDict, eplusInfo, customData=eplusCustomData)
    updateDifficulty(infoDict, eInfo, customData=eplusCustomData)
    createInfoDat(infoDict, 'test')


createTestFolder()
