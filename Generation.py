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
SLIDER_TIMING = 1/16

def initialize():
    mapList = open('map_list.txt', 'r')
    if not os.path.exists('map\\'):
        os.mkdir('map\\')
    if os.path.exists('map\\zipped'):
        os.remove('map\\zipped')
    if os.path.exists('map\\currentMap'):
        shutil.rmtree('map\\currentMap')
    return mapList
# download map
# read through map
# delete map


def downloadMap(bshash):
    url = 'https://r2cdn.beatsaver.com/' + bshash + '.zip'
    r = requests.get(url, allow_redirects=True)
    open('map\\zipped', 'wb').write(r.content)
    with zipfile.ZipFile('map\\zipped', 'r') as zip_ref:
        zip_ref.extractall('map\\currentMap')
        zip_ref.close()


def findDiffs():
    path = 'map\\currentMap\\'
    info = open(path+'Info.dat')
    infoDAT = json.load(info)
    standardIndex = -1
    for i in range(len(infoDAT['_difficultyBeatmapSets'])):
        if infoDAT['_difficultyBeatmapSets'][i]['_beatmapCharacteristicName'] == 'Standard':
            standardIndex = i
            break
    print(infoDAT['_songName'])
    if standardIndex == -1:
        return []
    return [e["_beatmapFilename"] for e in infoDAT['_difficultyBeatmapSets'][standardIndex]['_difficultyBeatmaps']]


# def readDiffs(diffNameList):
#     for diff in diffNameList:
#         print(diff[:-4])
#         # JSON of the last notes for each hand
#         lastJSON = [None, None]
#         # names of the last notes for each hand
#         lastNames = ['', '']

#         diffDAT = open('map\\currentMap\\'+diff, 'r')
#         d = json.load(diffDAT)
#         diffDAT.close()

#         for note in d['_notes']:
#             ty = note['_type']
#             # ignore all notes not on either hand
#             if ty > 1:
#                 continue
#             elif lastJSON[ty] is None:
#                 lastJSON[ty] = note
#                 lastNames[ty] = nameof(note)
#             else:
#                 # check for stack/window/slider/DD , if so skip
#                 if lastJSON[ty]['_time']+SLIDER_TIMING >= note['_time'] or lastNames[ty] == nameof(note):
#                     continue
#                 # otherwise make a chain from the last note to this one
#                 else:
#                     chainName = lastNames[ty] + ' ' + nameof(note)
#                     if chainName in nD.keys():
#                         nD[chainName] += 1
#                     else:
#                         nD[chainName] = 1
#                     lastJSON[ty] = note
#                     lastNames[ty] = nameof(note)


def readDiffs(diffNameList, folder='map\\currentMap\\'):
    for diff in diffNameList:
        print(diff[:-4])
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
    if os.path.exists('map\\zipped'):
        os.remove('map\\zipped')
    if os.path.exists('map\\currentMap'):
        shutil.rmtree('map\\currentMap')

def generateHashList():
    mapList = open('map_list.txt', 'w')
    date = '2020-09-11T00%3A00%3A00%2B00%3A00'
    while True: 
        all_curated_maps_s = requests.get('https://api.beatsaver.com/maps/latest?after=' + date + '&automapper=false&sort=CURATED')
        all_curated_maps = json.loads(all_curated_maps_s.text)
        for map in all_curated_maps['docs']:
            hash = map['versions'][0]['hash']
            mapList.write(hash + '\n')
        date = all_curated_maps['docs'][0]['lastPublishedAt'].replace(':', '%3A')[:-5] + '%2B00%3A00'
        # print(date)
        # print(all_curated_maps['docs'][0]['lastPublishedAt'])
        time.sleep(1)
        if len(all_curated_maps['docs']) != 20:
            break



generateHashList()
# mapList = initialize()
# for beatMap in mapList:
#     downloadMap(beatMap[:-1])
#     diffs = findDiffs()
#     readDiffs(diffs)
#     deleteMap()
#     time.sleep(.5)
# # readDiffs(os.listdir('speed'), 'speed\\')
# totals = open('note_totals.txt', 'w')
# sort = sorted(nD.items(), key=lambda kv: -kv[1])
# for key, value in sort:
#     totals.write(key + ': ' + str(value) + '\n')
