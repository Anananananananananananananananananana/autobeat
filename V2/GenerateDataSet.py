import os
import shutil
import time
import zipfile
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
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "dnt": "1",
    "if-none-match": "W/\"5bb-1w7PpBYUYHeYpyYe6WV2MPmiJj0\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/88.0.4324.104 Safari/537.36 "
}


def initialize():
    if os.path.exists('dlFolder'):
        shutil.rmtree('dlFolder')
    os.mkdir('dlFolder')


def downloadMap(bshash):
    url = 'https://r2cdn.beatsaver.com/' + bshash + '.zip'
    r = requests.get(url, allow_redirects=True)
    open('dlFolder\\zipped', 'wb').write(r.content)
    try:
        with zipfile.ZipFile('dlFolder\\zipped', 'r') as zip_ref:
            zip_ref.extractall('dlFolder\\currentMap')
            zip_ref.close()
    except:
        return False
    return True


def deleteMap():
    if os.path.exists('dlFolder\\zipped'):
        shutil.rmtree('dlFolder\\zipped')
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


def generateFromRanked(start_date='2020-10-09T00%3A00%3A00%2B00%3A00', end_date='2022-12-22T00%3A00%3A00%2B00%3A00', max_calls=1):
    initialize()
    counter = max_calls
    while counter != 0:
        counter -= 1
        mapList, end_date = generateHashList(start_date, end_date)
        for beatMap in mapList:
            time.sleep(0.5)
            downloaded = downloadMap(beatMap)
            if not downloaded:
                print('\nskipped: ' + beatMap)
                deleteMap()
                continue
            # diffs = findDiffs()
            diffs = None
            readDiffs(diffs)
            deleteMap()
        if len(mapList) != 20:
            break


def generateFromFolder(path):
    readDiffs(os.listdir(path), folder=path)


def readDiffs(diffNameList, folder='dlFolder\\currentMap\\'):
    train = open('train.txt', 'a')
    for diff in diffNameList:
        diffDAT = open(folder + diff, 'r')
        try:
            diffJSON = json.load(diffDAT)
            diffDAT.close()
        except:
            continue
        diffDAT.close()

        noteTime = diffJSON['_notes'][0]['_time']
        for note in diffJSON['_notes']:
            if note['_time'] != noteTime:
                noteTime = note['_time']
                train.write('\n')
            train.write(noteName(note)+' ')
        train.write('\n')
    train.close()


def noteName(JSON):
    coord = [['8', '9', 'a', 'b'],
             ['4', '5', '6', '7'],
             ['0', '1', '2', '3']]
    return coord[2 - JSON['_lineLayer']][JSON['_lineIndex']] + str(JSON['_cutDirection']) + str(JSON['_type'])


generateFromFolder('..\\speed\\')
