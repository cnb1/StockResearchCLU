import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import scraper
from colorama import Fore
import printFunctions as pf
import time
import threading
from tabulate import tabulate
from colorama import Fore
import pandas as pd


def run(list):
    isRun = True
    while isRun:
        ticker = input(Fore.YELLOW + pf.createConsole(list, 'stock') + Fore.WHITE)
        if ticker == "!q":
            isRun = False
        else:
            # start = time.time ()
            return_val_stats = [None]*2
            return_val_forecast = [None]*1
            #thread with returning df
            tstats = threading.Thread(target=scraper.generalStats, args=(ticker,return_val_stats))
            #thread with returning df

            #print the information here below
            tforecast = threading.Thread(target=scraper.forecastStock, args=(ticker,return_val_forecast))

            tstats.start()
            tforecast.start()
            tstats.join()
            tforecast.join()
            
            # df = pd.DataFrame(data=return_val_stats[0])
            print(Fore.WHITE + tabulate(return_val_stats[1], headers='keys', tablefmt="double_outline", showindex=False) + Fore.WHITE)
            print()
            print()
            print()
            print(Fore.LIGHTBLUE_EX + tabulate(return_val_stats[0], headers='keys', tablefmt="double_outline", showindex=False) + Fore.WHITE)
            print()
            # df = pd.DataFrame(data=return_val_forecast[0])
            print(Fore.LIGHTCYAN_EX + tabulate(return_val_forecast[0], headers='keys', tablefmt="double_outline", showindex=False) + Fore.WHITE)

            # end = time.time()

            # print("The time of execution of above program is :", (end-start) * 10**3, "ms")

        print()