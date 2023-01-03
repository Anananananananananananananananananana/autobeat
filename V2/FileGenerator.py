import json
import os
import tempfile
from pydub import AudioSegment


# Difficulty names and ranks recognized by Beat Saber
POSSIBLE_DIFF_NAMES = ['Easy', 'Normal', 'Hard', 'Expert', 'ExpertPlus']
DIFFICULTY_RANKS = {
    'Easy': 1,
    'Normal': 3,
    'Hard': 5,
    'Expert': 7,
    'ExpertPlus': 9
}


# Creates the folder that info.dat, difficulty, and song.ogg are placed into, if it does not already exist
def createMapFolder():
    pass


# Creates the appropriate info.dat
def createInfoDat():
    pass


# Create empty difficulty.dat files
def createDifficulties():
    pass


def exportAudioFile(filename: str):
    """
    Exports the audio file as song.ogg, and places it appropriately
    """
    with open(filename, "r") as audiofile:
        data = audiofile.read()
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(data)
    AudioSegment.from_mp3(f.name).export('export/result.ogg', format='ogg')
    f.close()