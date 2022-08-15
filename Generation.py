import os
import shutil
import time
import zipfile
from Utils import noteName as nameof
import pip
try:
    import requests
    import json
except:
    pip.main(['install', 'json'])
    pip.main(['install', 'requests'])
    import json
    import requests
headers = {
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-language": "en-US,en;q=0.9",
"cache-control": "max-age=0",
"dnt": "1",
"if-none-match": "W/\"5bb-1w7PpBYUYHeYpyYe6WV2MPmiJj0\"",
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "none",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
}

nD = dict()
SLIDER_TIMING = 1/13

def initialize():
    if not os.path.exists('dlFolder\\'):
        os.mkdir('dlFolder\\')
    if os.path.exists('dlFolder\\zipped'):
        os.remove('dlFolder\\zipped')
    if os.path.exists('dlFolder\\currentMap'):
        shutil.rmtree('dlFolder\\currentMap')
    return mapList
# download dlFolder
# read through dlFolder
# delete dlFolder


def downloadMap(bshash):
    url = 'https://r2cdn.beatsaver.com/' + bshash + '.zip'
    r = requests.get(url, allow_redirects=True)
    open('dlFolder\\zipped', 'wb').write(r.content)
    with zipfile.ZipFile('dlFolder\\zipped', 'r') as zip_ref:
        zip_ref.extractall('dlFolder\\currentMap')
        zip_ref.close()


def findDiffs():
    path = 'dlFolder\\currentMap\\'
    info = open(path+'Info.dat')
    infoDAT = json.load(info)
    standardIndex = -1
    for i in range(len(infoDAT['_difficultyBeatmapSets'])):
        if infoDAT['_difficultyBeatmapSets'][i]['_beatmapCharacteristicName'] == 'Standard':
            standardIndex = i
            break
    print(infoDAT['_songName']+'\n')
    if standardIndex == -1:
        return []
    diffList = []
    for beatMap in infoDAT['_difficultyBeatmapSets'][standardIndex]['_difficultyBeatmaps']:
        if '_customData' in beatMap.keys() and '_requirements' in beatMap['_customData'].keys():
            if 'Noodle Extensions' in beatMap['_customData']['_requirements'] or 'Mapping Extensions' in beatMap['_customData']['_requirements']:
                continue
        diffList.append(beatMap['_beatmapFilename'])
    return diffList


def readDiffs(diffNameList, folder='dlFolder\\currentMap\\'):
    for diff in diffNameList:
        # JSON of the last notes for each hand
        lastJSON = [None, None]
        # names of the last notes for each hand
        lastNames = ['', '']

        diffDAT = open(folder + diff, 'r')
        d = json.load(diffDAT)
        diffDAT.close()

        for note in d['_notes']:
            ty = note['_type']
            # ignore all notes not on either hand
            if ty > 1:
                continue
            elif lastJSON[ty] is None:
                lastJSON[ty] = note
                lastNames[ty] = nameof(note)
            else:
                # check for stack/window/slider/DD , if so skip
                if lastJSON[ty]['_time']+SLIDER_TIMING >= note['_time'] or lastNames[ty] == nameof(note):
                    continue
                # otherwise make a chain from the last note to this one
                else:
                    chainName = lastNames[ty] + ' ' + nameof(note)
                    if chainName in nD.keys():
                        nD[chainName] += 1
                    else:
                        nD[chainName] = 1
                    lastJSON[ty] = note
                    lastNames[ty] = nameof(note)


def deleteMap():
    if os.path.exists('dlFolder\\zipped'):
        os.remove('dlFolder\\zipped')
    if os.path.exists('dlFolder\\currentMap'):
        shutil.rmtree('dlFolder\\currentMap')


def generateHashList(date):
    mapList = []
    all_curated_maps_s = requests.get('https://api.beatsaver.com/maps/latest?after=' + date + '&automapper=false&sort=CURATED')
    all_curated_maps = json.loads(all_curated_maps_s.text)
    for map in all_curated_maps['docs']:
        hash = map['versions'][0]['hash']
        mapList.append(hash)
    end = all_curated_maps['docs'][0]['lastPublishedAt'].replace(':', '%3A')[:-5] + '%2B00%3A00'
    return mapList, end



counter = 0
date = '2020-09-11T00%3A00%3A00%2B00%3A00'
while counter < 1:
    counter += 1
    mapList, date = generateHashList(date)
    for beatMap in mapList:
        downloadMap(beatMap)
        diffs = findDiffs()
        readDiffs(diffs)
        deleteMap()
        time.sleep(.5)
    if len(mapList) != 20:
        break

totals = open('note_totals.txt', 'w')
sort = sorted(nD.items(), key=lambda kv: -kv[1])
for key, value in sort:
    totals.write(key + ': ' + str(value) + '\n')

