import os
currentdir = os.path.dirname(os.path.realpath(__file__))
import pickle as p
# import cache.cacheObject as co
from datetime import date
import datetime
from colorama import Fore
import json
from rich.console import Console
import time


CACHE_UPDATE_TIME_IN_DAYS = 7
__cache = {}
__toStore = {}

class CacheTable:
    def __init__(self, table, time):
        self.table = table
        self.time = time

    def getTable(self):
        return self.table

    def getTime(self):
        return self.time

def load():
    isRemoved = False
    if os.path.exists(currentdir + '/cache.txt') and os.stat(currentdir + '/cache.txt').st_size != 0:
        print(Fore.GREEN + '[Cache file exists]'+ Fore.WHITE)
        with open(currentdir + '/cache.txt', 'r') as testpick:
            data = json.load(testpick)

            dict = {}
            dictStore = {}

            for i in data:
                o = CacheTable(data[i]['table'], datetime.datetime.strptime(data[i]['time'], '%Y-%m-%d').date())
                dict[i] = o
                dictStore[i] = data[i]

            # need to filter out the dict for outdated times
            today = date.today()
            d = datetime.timedelta(CACHE_UPDATE_TIME_IN_DAYS)
            check = today - d
            toDelete = []

            for key in dict.keys():
                if check > dict[key].getTime():
                    toDelete.append(key)
                
            for key in toDelete:
                print(Fore.RED + 'Removing : ' + key + Fore.WHITE)
                isRemoved = True
                dict.pop(key, None)
                dictStore.pop(key, None)
            
            __cache.update(dict)
            __toStore.update(dictStore)

    else:
        print(Fore.RED + '[Cache file doesn`t exists OR is empty]'+ Fore.WHITE)

    return isRemoved


def save():
    console = Console()

    with console.status("[bold yellow]Saving cache...") as status:
        time.sleep(1)
        with open(currentdir + '/cache.txt', 'w') as jsonload:
            jsonload.write(json.dumps(__toStore))


def createKey(ticker, filename):
    return ticker + '-' + filename

def checkObjKey(ticker, filename):
    key = createKey(ticker, filename)

    if key in __cache:
        return True
    else:
        return False
    
def setObj(ticker, filename, table):
    key = createKey(ticker, filename)
    if not (checkObjKey(ticker, filename)):
        o = CacheTable(table, date.today())
        ostore = CacheTable(table, str(date.today()))
        __cache[key] = o
        __toStore[key] = ostore.__dict__
        save()


def getObj(ticker, filename):
    if checkObjKey(ticker, filename):
        key = createKey(ticker, filename)
        return __cache[key]
    else:
        return None