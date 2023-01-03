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


def mkFiles(songfile: str, songInfo, mapInfo, difficulties):
    """
    Main method that calls the others as necessary
    :param songfile: File path to the song file
    :param songInfo: JSON object that holds the song information such as Artist, Title, BPM etc.
    :param mapInfo: JSON object that holds the preview Start and Duration, as well as the Environment
    :param difficulties: A list of difficulty JSON objects ordered from Easy to ExpertPlus
    :return:
    """
    createMapFolder()
    createInfoDat(songInfo, mapInfo, difficulties)
    createDifficulties(difficulties)
    exportAudioFile(songfile)


def createMapFolder():
    """
    Creates the folder that info.dat, difficulty files, and song.ogg are placed into
    """
    if os.path.exists('export'):
        shutil.rmtree('export')
    os.mkdir('export')


def createInfoDat(songInfo, mapInfo, difficulties):
    """
    Creates the appropriate info.dat
    :param songInfo: JSON object that holds the song information such as Artist, Title, BPM etc.
    :param mapInfo: JSON object that holds the preview Start and Duration, as well as the Environment
    :param difficulties: A list of difficulty JSON objects ordered from Easy to ExpertPlus
    """
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
        '_songFilename': 'song.ogg',
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


def createDifficulties(difficulties):
    """
    Create empty difficulty.dat files
    :param difficulties: A list of difficulty JSON objects ordered from Easy to ExpertPlus
    """
    for diff in difficulties:
        open('export\\' + diff['diff'] + diff['type'] + '.dat', 'w')


def exportAudioFile(songfile: str):
    """
    Exports the audio file as song.ogg, and places it appropriately
    :param songfile: File path to the song file
    """
    with open(songfile, "r") as audiofile:
        data = audiofile.read()
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(data)
    AudioSegment.from_mp3(f.name).export('export\\song.ogg', format='ogg')
    f.close()


