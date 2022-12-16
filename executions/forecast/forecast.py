import os, sys
from tabnanny import check
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
import cache.stockCache as sc

FILENAME = 'forecast'
METRICS = 'Metrics'
VALUES = 'Values'

def __createValuesAndMetrics(header, values, forecast):
    dataMetric = []
    dataValue = []

    dataMetric.append('Stock')
    dataValue.append(header.head(1).iloc[0].iloc[0])

    for i in range(len(values.columns)):
        dataMetric.append(values.columns[i])
        dataValue.append(values.iloc[0].iloc[i])
    
    for i in range(len(forecast.columns)):
        dataMetric.append(forecast.columns[i])
        dataValue.append(forecast.iloc[0].iloc[i])

    data = {
        METRICS: dataMetric,
        VALUES: dataValue
    }

    return data

def __createDataframe(data):
    dfdata = pd.DataFrame(data)
    return dfdata

def __printDataframe(df):
    console = Console()
    table = Table(title=df[VALUES].iloc[0])

    table.add_column(METRICS, style='dodger_blue2', no_wrap=True)
    table.add_column(VALUES, style='deep_sky_blue1', no_wrap=True)

    for i in range(len(df.index)):
        table.add_row(df[METRICS].iloc[i], df[VALUES].iloc[i])


    print()
    console.print(table)

def run(list):
    isRun = True
    console = Console()

    
    while isRun: #and (console.status("[bold green]Fetching data...") as status):
        ticker = input(Fore.YELLOW + pf.createConsole(list, 'forecast/[Enter Ticker]') + Fore.WHITE)
        if ticker == "!q":
            isRun = False
        else:
        
            # here check cache for dataframe
            start = time.time()

            #local cache feature
            if sc.checkObjKey(ticker, FILENAME):
                print()
                df = __createDataframe(sc.getObj(ticker, FILENAME).getTable())
                __printDataframe(df)
                print()
                print()
                end = time.time()
                print("The time of execution of above program is :", (end-start) * 10**3, "ms")
            else :
                with console.status("[bold green]Fetching data...") as status:
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

                    if return_val_forecast[0] is None:
                        continue

                # create the data frame here then call a print dataframe to table function
                datadict = __createValuesAndMetrics(return_val_stats[1], return_val_stats[0],return_val_forecast[0])
                df = __createDataframe(datadict)
                # this dataframe is the one that gets stored and see if its less memory

                # turn df into table and print it
                __printDataframe(df)

                end = time.time()
                print("The time of execution of above program is :", (end-start) * 10**3, "ms")
                print()
                print()

                # store the data frames then write a function that translates these dataframs
                sc.setObj(ticker, FILENAME, datadict)