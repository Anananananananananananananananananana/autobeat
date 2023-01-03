import json
import os
import tempfile
from pydub import AudioSegment
import shutil

# Difficulty names and ranks recognized by Beat Saber
POSSIBLE_DIFF_NAMES = ['Easy', 'Normal', 'Hard', 'Expert', 'ExpertPlus']
DIFFICULTY_RANKS = {
    'Easy': 1,
    'Normal': 3,
    'Hard': 5,
    'Expert': 7,
    'ExpertPlus': 9
}


# Main method that calls the others as necessary
# difficulties should be sorted from Easy to ExpertPlus

def mkFiles(songfile, songInfo, mapInfo, difficulties):
    createMapFolder()
    createInfoDat(songInfo, mapInfo, difficulties)
    createDifficulties(difficulties)
    exportAudioFile(songfile)


# Creates the folder that info.dat, difficulty, and song.ogg are placed into
def createMapFolder():
    if os.path.exists('export'):
        shutil.rmtree('export')
    os.mkdir('export')


# Creates the appropriate info.dat
def createInfoDat(songInfo, mapInfo, difficulties):
    f = open('export\\Info.dat', 'w')

    # Creating barebones JSON version of Info.dat
    infoJSON = {
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
        '_difficultyBeatmapSets': [
            {
                "_beatmapCharacteristicName": "Standard",
                "_difficultyBeatmaps": []
            }
        ]
    }

    for diff in difficulties:
        difficultyJSON = {
            "_difficulty": diff['diff'],
            "_difficultyRank": DIFFICULTY_RANKS[diff['diff']],
            "_beatmapFilename": diff['diff'] + diff['type'] + '.dat',
            "_noteJumpMovementSpeed": diff['njs'],
            "_noteJumpStartBeatOffset": diff['offset']
        }
        infoJSON['_difficultyBeatmapSets'][0]['_difficultyBeatmaps'].append(difficultyJSON)
    f.write(json.dumps(infoJSON, indent=2))
    f.close()


# Create empty difficulty.dat files
def createDifficulties(difficulties):
    for diff in difficulties:
        open('export\\' + diff['diff'] + diff['type'] + '.dat', 'w')


def exportAudioFile(songfile: str):
    """
    Exports the audio file as song.ogg, and places it appropriately
    """
    with open(songfile, "r") as audiofile:
        data = audiofile.read()
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(data)
    AudioSegment.from_mp3(f.name).export('export\\song.ogg', format='ogg')
    f.close()


