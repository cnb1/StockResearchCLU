import os
currentdir = os.path.dirname(os.path.realpath(__file__))
from copyreg import pickle
import pickle as p
import cache.cacheObject as co
from datetime import date
import datetime

cache = {}

def load(self):
    print('loading files')
    with open(currentdir + '/cache.pickle', 'rb') as testpick:
        dict = p.load(testpick)

    # need to filter out the dict for outdated times
    today = date.today()
    d7 = datetime.timedelta(7)
    weekCheck = today - d7
    toDelete = []

    # now update
    cache.update(dict)

    for key in dict.keys():
        if weekCheck > key:
            toDelete.append(key)
        
    for key in toDelete:
        dict.pop(key, None)
    
    cache.update(dict)


def save():
    print('saving files')
    with open(currentdir + '/cache.pickle', 'wb') as write_cache:
        p.dump(cache, write_cache)

def createKey(ticker, filename):
    return ticker + '-' + filename

def checkObjKey(ticker, filename):
    key = createKey(ticker, filename)
    print('checking ', key)

    if key in cache:
        return True
    else:
        return False
    
def setObj(ticker, filename, table):
    key = createKey(ticker, filename)
    print('setting key ', key)
    if not (checkObjKey(ticker, filename)):
        o = co(table, date.today())
        cache[key] = o
        save()


def getObj(ticker, filename):
    if checkObjKey(ticker, filename):
        key = createKey(ticker, filename)
        return cache[key]
    else:
        return None