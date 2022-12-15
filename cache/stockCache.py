import os
currentdir = os.path.dirname(os.path.realpath(__file__))
import pickle as p
import cache.cacheObject as co
from datetime import date
import datetime
from colorama import Fore

import sys
sys.setrecursionlimit(10000)
CACHE_UPDATE_TIME_IN_DAYS = 7
cache = {}

def load():
    if os.path.exists(currentdir + '/cache.pickle') and os.stat(currentdir + '/cache.pickle').st_size != 0:
        print(Fore.GREEN + '[Cache file exists]'+ Fore.WHITE)
        with open(currentdir + '/cache.pickle', 'rb') as testpick:
            dict = p.load(testpick)

            print('testing')
            print(dict)

            # need to filter out the dict for outdated times
            today = date.today()
            d = datetime.timedelta(CACHE_UPDATE_TIME_IN_DAYS)
            check = today - d
            toDelete = []

            # now update
            cache.update(dict)

            for key in dict.keys():
                if check > dict[key].getTime():
                    toDelete.append(key)
                
            for key in toDelete:
                dict.pop(key, None)
            
            cache.update(dict)
    else:
        print(Fore.RED + '[Cache file doesn`t exists OR is empty]'+ Fore.WHITE)


def save():
    print('saving files')
    with open(currentdir + '/cache.pickle', 'wb') as write_cache:
        p.dump(cache, write_cache, p.HIGHEST_PROTOCOL)

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
        o = co.CacheTable(table, date.today())
        cache[key] = o
        save()


def getObj(ticker, filename):
    if checkObjKey(ticker, filename):
        key = createKey(ticker, filename)
        return cache[key]
    else:
        return None