from copyreg import pickle
from inspect import getfile
import pickle as p
import cache.cacheObject as co
from datetime import date
import datetime

cache = {}

def load():
    print('loading files')

def save():
    print('saving files')
    pickle.dump()

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


def getObj(ticker, filename):
    if checkObjKey(ticker, filename):
        key = createKey(ticker, filename)
        return cache[key]
    else:
        return None