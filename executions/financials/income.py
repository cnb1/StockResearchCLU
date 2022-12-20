import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parentdir)
sys.path.append(currentdir)

from colorama import Fore
import time
import printFunctions as pf
from rich.console import Console
from rich.table import Table
import cache.stockCache as sc
import scraper

# grab data from scraper
# store it all in a dict to be stored and grabbed and printed

FILENAME = 'income'

def __createDictToStore(title, header, rows):
    data = {
        'title': title,
        'header': header,
        'rows': rows
    }

    return data

def __dictToTable(data):
    console = Console()
    table = Table(title=data['title'] + ' Income Statement', expand=True, header_style='chartreuse1',
                    show_lines=True)

    for i in range(len(data['header'])):
        table.add_column(data['header'][i], style='bright_white', no_wrap=True)
    
    for i in range(len(data['rows'])):
        table.add_row(data['rows'][i][0], data['rows'][i][1],
                            data['rows'][i][2], data['rows'][i][3],
                            data['rows'][i][4], data['rows'][i][5])

    console.print(table)


def run(list):
    isRun = True
    console = Console()

    
    while isRun: #and (console.status("[bold green]Fetching data...") as status):
        ticker = input(Fore.YELLOW + pf.createConsole(list, 'forecast/[Enter Ticker]') + Fore.WHITE)
        if ticker == "!q" or ticker == "..":
            isRun = False
        else:
            # here check cache for dataframe
            start = time.time()
            
            # check if the income is already in the cache
            if sc.checkObjKey(ticker, FILENAME) :
                print()
                tabledict = sc.getObj(ticker, FILENAME).getTable()
                __dictToTable(tabledict)
                print('\n')
            else:
                title, header, rows = scraper.getIncome(ticker)

                # turn rows and columns into table
                data = __createDictToStore(title, header, rows)
                # print the data
                print()
                __dictToTable(data)
                print('\n')

                #store in cache
                sc.setObj(ticker, FILENAME, data)


            end = time.time()
            print("The time of execution of above program is :", (end-start) * 10**3, "ms")