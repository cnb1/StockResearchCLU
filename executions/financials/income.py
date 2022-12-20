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

def run(list):
    print('income')
    isRun = True
    console = Console()

    
    while isRun: #and (console.status("[bold green]Fetching data...") as status):
        ticker = input(Fore.YELLOW + pf.createConsole(list, 'forecast/[Enter Ticker]') + Fore.WHITE)
        if ticker == "!q" or ticker == "..":
            isRun = False
        else:
            # here check cache for dataframe
            start = time.time()
            
            scraper.getIncome(ticker)

            end = time.time()
            print("The time of execution of above program is :", (end-start) * 10**3, "ms")