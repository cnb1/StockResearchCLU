import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import scraper
from colorama import Fore
import printFunctions as pf



def stockForecast(list):
    # TODO create looping for this inputs
    isRun = True
    while isRun:
        ticker = input(Fore.YELLOW + pf.createConsole(list, 'stock') + Fore.WHITE)
        if ticker == "!q":
            isRun = False
        else:
            scraper.forecast(ticker)

        print()