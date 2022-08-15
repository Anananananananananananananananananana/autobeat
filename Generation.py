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
# download dlFolder
# read through dlFolder
# delete dlFolder


def downloadMap(bshash):
    url = 'https://r2cdn.beatsaver.com/' + bshash + '.zip'
    r = requests.get(url, allow_redirects=True)
    open('dlFolder\\zipped', 'wb').write(r.content)
    try:
        with zipfile.ZipFile('dlFolder\\zipped', 'r') as zip_ref:
            zip_ref.extractall('dlFolder\\currentMap')
            zip_ref.close()
        return False
    except:
        return False
    return True


def findDiffs():
    path = 'dlFolder\\currentMap\\'
    info = open(path+'Info.dat')
    infoDAT = json.load(info)
    standardIndex = -1
    for i in range(len(infoDAT['_difficultyBeatmapSets'])):
        if infoDAT['_difficultyBeatmapSets'][i]['_beatmapCharacteristicName'] == 'Standard':
            standardIndex = i
            break
    print('\n', infoDAT['_songName'], ' - ', infoDAT['_levelAuthorName'], sep='')
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
        print(diff[:-12], end=' ')
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
    print()


def deleteMap():
    if os.path.exists('dlFolder\\zipped'):
        os.remove('dlFolder\\zipped')
    if os.path.exists('dlFolder\\currentMap'):
        shutil.rmtree('dlFolder\\currentMap')


def generateHashList(start_date, end_date):
    mapList = []
    ranked_maps_s = requests.get('https://api.beatsaver.com/search/text/0?from=' + start_date +
     '&noodle=false&ranked=true&sortOrder=Latest&to=' + end_date)
    ranked_maps = json.loads(ranked_maps_s.text)
    for map in ranked_maps['docs']:
        hash = map['versions'][0]['hash']
        mapList.append(hash)
    end = ranked_maps['docs'][-1]['createdAt'].replace(':', '%3A')[:-5] + '%2B00%3A00'
    return mapList, end



def assignParities():
    parityDict = dict()
    techList = []
    cutDict = {
        '1': {
            '0': 1,
            '1': 0,
            '2': 0,
            '3': 1,
            '4': 1,
            '5': 1,
            '6': 0,
            '7': 0
        },
        '0': {
            '0': 1,
            '1': 0,
            '2': 1,
            '3': 0,
            '4': 1,
            '5': 1,
            '6': 0,
            '7': 0
        }
    }
    for key in nD.keys():
        first = key[:3]
        last = key[4:]
        bad_list = [{'1', '7'}, {'1', '6'}, {'4', '0'}, {'5', '0'}, {'5', '3'}, {'7', '3'}, {'6', '2'}, {'4', '2'}]
        if first[1] == '8' or last[1] == '8' or {first[1], last[1]} in bad_list:
            continue
        fp = cutDict[first[2]][first[1]]
        lp = cutDict[last[2]][last[1]]
        if fp == lp:
            techList.append(key)
        else:
            if first+str(fp) in parityDict.keys():
                parityDict[first+str(fp)].append(last+str(lp))
            else:
                parityDict[first + str(fp)] = [last + str(lp)]
    tech = open('tech.txt', 'w')
    good = open('good.txt', 'w')
    for chain in techList:
        tech.write(chain + '\n')
    for key, value in parityDict.items():
        good.write('\''+key + '\': ' + str(value) + ',\n')

initialize()
counter = 0
start_date = '2020-10-09T00%3A00%3A00%2B00%3A00'
end_date = '2022-08-13T00%3A00%3A00%2B00%3A00'
while counter < 1:
    counter += 1
    mapList, end_date = generateHashList(start_date, end_date)
    for beatMap in mapList:
        time.sleep(.5)
        downloaded = downloadMap(beatMap)
        if not downloaded:
            print('\nskipped: '+beatMap)
            deleteMap()
            continue
        diffs = findDiffs()
        readDiffs(diffs)
        deleteMap()
    if len(mapList) != 20:
        break
totals = open('note_totals.txt', 'w')
sort = sorted(nD.items(), key=lambda kv: -kv[1])
for key, value in sort:
    totals.write(key + ': ' + str(value) + '\n')
assignParities()

