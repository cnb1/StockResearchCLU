import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parentdir)
sys.path.append(currentdir)

import scraper
from colorama import Fore
import printFunctions as pf
import time
import threading
from tabulate import tabulate
from colorama import Fore
import pandas as pd
from rich.console import Console
from rich.table import Table


def run(list):
    isRun = True
    console = Console()

    
    while isRun: #and (console.status("[bold green]Fetching data...") as status):
        ticker = input(Fore.YELLOW + pf.createConsole(list, 'forecast/[Enter Ticker]') + Fore.WHITE)
        if ticker == "!q":
            isRun = False
        else:
            with console.status("[bold green]Fetching data...") as status:

                start = time.time()
                return_val_stats = [None]*2
                return_val_forecast = [None]*1
                #thread with returning df
                tstats = threading.Thread(target=scraper.generalStats, args=(ticker,return_val_stats))
                #thread with returning df
                tforecast = threading.Thread(target=scraper.forecastStock, args=(ticker,return_val_forecast))

                tstats.start()
                tforecast.start()
                tstats.join()
                tforecast.join()
            

                end = time.time()

                table2 = Table(title=return_val_stats[1].head(1).iloc[0].iloc[0])

                table2.add_column('Metric', style='dodger_blue2', no_wrap=True)
                table2.add_column('Value', style='deep_sky_blue1', no_wrap=True)

                for i in range(len(return_val_stats[0].columns)):
                    table2.add_row(return_val_stats[0].columns[i], return_val_stats[0].iloc[0].iloc[i])

                for i in range(len(return_val_forecast[0].columns)):
                    table2.add_row(return_val_forecast[0].columns[i], return_val_forecast[0].iloc[0].iloc[i])

                print()
                console.print(table2)

                print("The time of execution of above program is :", (end-start) * 10**3, "ms")
                print()
                print()


if __name__ == '__main__':
    print('hello')