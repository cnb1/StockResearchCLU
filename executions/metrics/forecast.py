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
import cache.stockCache as sc
import re
import pyfiglet

FILENAME = 'forecast'
METRICS = 'Metrics'
VALUES = 'Values'
SCALE_VAL = 10

MIN_FORECAST = 'Min Forecast'
AVG_FORECAST = 'Avg Forecast'
MAX_FORECAST = 'Max Forecast'

MIN_FORECAST_T = 'Min Proj.'
AVG_FORECAST_T = 'Avg Proj.'
MAX_FORECAST_T = 'Max Proj.'

A1YF = 'Avg 1 year Forecast'
A2YF = 'Avg 2 year Forecast'
A3YF = 'Avg 3 year Forecast'

A1YFT = '1Y Avg Proj.'
A2YFT = '2Y Avg Proj.'
A3YFT = '3Y Avg Proj.'

TITLE_YRS = "(Current, 1 Year, 2 Year, 3 Year)"

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
        if df[METRICS].iloc[i] != 'Stock':
            table.add_row(df[METRICS].iloc[i], df[VALUES].iloc[i])


    print()
    console.print(table)



def  __dataframeToDict(df):
        d = {}
        for i in df.values:
            d[i[0]]=i[1]
        return d

def __dollarsToFloat(s):
    s = round(float(re.sub(r'[^0-9.-]', '', s)), 2)
    return s


def __createForecastTables(ticker, dfdict):
    ## price 
    priceforecastVal = [__dollarsToFloat(dfdict[ticker + ' Price']), __dollarsToFloat(dfdict[MIN_FORECAST]), 
                        __dollarsToFloat(dfdict[AVG_FORECAST]), __dollarsToFloat(dfdict[MAX_FORECAST])]

    priceforecastLabel = [ticker + ' Price : ' + str(__dollarsToFloat(dfdict[ticker + ' Price'])),
                            MIN_FORECAST_T + ' : ' + str(__dollarsToFloat(dfdict[MIN_FORECAST])),
                            AVG_FORECAST_T + ' : ' + str(__dollarsToFloat(dfdict[AVG_FORECAST])),
                            MAX_FORECAST_T + ' : ' + str(__dollarsToFloat(dfdict[MAX_FORECAST]))]

    priceTable = pf.createChart(ticker + ' Price Forecast ' + TITLE_YRS, priceforecastLabel, priceforecastVal)


    ## revenue
    revforecastVal = [__dollarsToFloat(dfdict['Revenue']), __dollarsToFloat(dfdict[A1YF + ' Rev']), 
                        __dollarsToFloat(dfdict[A2YF + ' Rev']), __dollarsToFloat(dfdict[A3YF + ' Rev'])]
    
    revforecastLabel = ['Revenue : ' + str(__dollarsToFloat(dfdict['Revenue'])),
                        A1YFT + ' : ' + str(__dollarsToFloat(dfdict[A1YF + ' Rev'])),
                        A2YFT + ' : ' + str(__dollarsToFloat(dfdict[A2YF + ' Rev'])),
                        A3YFT + ' : ' + str(__dollarsToFloat(dfdict[A3YF + ' Rev']))]

    revenueTable = pf.createChart(ticker + ' Revenue Forecast ' + TITLE_YRS, revforecastLabel, revforecastVal)

    ## EPS
    epsforecastVal = [__dollarsToFloat(dfdict['EPS']), __dollarsToFloat(dfdict[A1YF + ' EPS']), 
                        __dollarsToFloat(dfdict[A2YF + ' EPS']), __dollarsToFloat(dfdict[A3YF + ' EPS'])]
    
    epsforecastLabel = ['EPS : ' + str(__dollarsToFloat(dfdict['EPS'])),
                        A1YFT + ' : ' + str(__dollarsToFloat(dfdict[A1YF + ' EPS'])),
                        A2YFT + ' : ' + str(__dollarsToFloat(dfdict[A2YF + ' EPS'])),
                        A3YFT + ' : ' + str(__dollarsToFloat(dfdict[A3YF + ' EPS']))]

    epsTable = pf.createChart(ticker + ' EPS Forecast ' + TITLE_YRS, epsforecastLabel, epsforecastVal)

    ## P/E
    peforecastVal = [__dollarsToFloat(dfdict[ticker + ' Price'])/__dollarsToFloat(dfdict['EPS']),
                    __dollarsToFloat(dfdict[ticker + ' Price'])/__dollarsToFloat(dfdict[A1YF + ' EPS']),
                    __dollarsToFloat(dfdict[ticker + ' Price'])/__dollarsToFloat(dfdict[A2YF + ' EPS']),
                    __dollarsToFloat(dfdict[ticker + ' Price'])/__dollarsToFloat(dfdict[A3YF + ' EPS'])]
    
    peforecastLabel = ['P/E : ' + str(round(__dollarsToFloat(dfdict[ticker + ' Price'])/__dollarsToFloat(dfdict['EPS']), 2)),
                        A1YFT + ' : ' + str(round(__dollarsToFloat(dfdict[ticker + ' Price'])/__dollarsToFloat(dfdict[A1YF + ' EPS']), 2)),
                        A2YFT + ' : ' + str(round(__dollarsToFloat(dfdict[ticker + ' Price'])/__dollarsToFloat(dfdict[A2YF + ' EPS']), 2)),
                        A3YFT + ' : ' + str(round(__dollarsToFloat(dfdict[ticker + ' Price'])/__dollarsToFloat(dfdict[A3YF + ' EPS']), 2))]

    peTable = pf.createChart(ticker + ' P/E Forecast ' + TITLE_YRS, peforecastLabel, peforecastVal)

    ## P/S
    psforecastVal = [__dollarsToFloat(dfdict['Market Cap'])/__dollarsToFloat(dfdict['Revenue']),
                    __dollarsToFloat(dfdict['Market Cap'])/__dollarsToFloat(dfdict[A1YF + ' Rev']),
                    __dollarsToFloat(dfdict['Market Cap'])/__dollarsToFloat(dfdict[A2YF + ' Rev']),
                    __dollarsToFloat(dfdict['Market Cap'])/__dollarsToFloat(dfdict[A3YF + ' Rev'])]
    
    psforecastLabel = ['P/S : ' + str(round(__dollarsToFloat(dfdict['Market Cap'])/__dollarsToFloat(dfdict['Revenue']), 2)),
                        A1YFT + ' : ' + str(round(__dollarsToFloat(dfdict['Market Cap'])/__dollarsToFloat(dfdict[A1YF + ' Rev']), 2)),
                        A2YFT + ' : ' + str(round(__dollarsToFloat(dfdict['Market Cap'])/__dollarsToFloat(dfdict[A2YF + ' Rev']), 2)),
                        A3YFT + ' : ' + str(round(__dollarsToFloat(dfdict['Market Cap'])/__dollarsToFloat(dfdict[A3YF + ' Rev']), 2))]

    psTable = pf.createChart(ticker + ' P/S Forecast ' + TITLE_YRS, psforecastLabel, psforecastVal)






    return priceTable, revenueTable, epsTable, peTable, psTable

def __printCharts(console, price, rev, eps, pe, ps):
    table = Table(leading=2, show_header=False, show_edge=False)
    table.add_column('PRICE PROJECTION', justify='center')
    table.add_column('REVENUE PROJECTION', justify='center')
    table.add_row(price)
    table.add_row(rev, eps)
    table.add_row(ps, pe)
    ## add row EPS
    console.print(table)




def run(context):
    isRun = True
    console = Console()

    
    while isRun: #and (console.status("[bold green]Fetching data...") as status):
        ticker = input(Fore.YELLOW + pf.createConsole(context, 'forecast/[Enter Ticker]') + Fore.WHITE)
        if ticker == "!q" or ticker == "..":
            isRun = False
        else:
        
            # here check cache for dataframe
            start = time.time()

            #local cache feature
            if sc.checkObjKey(ticker, FILENAME):
                print()
                df = __createDataframe(sc.getObj(ticker, FILENAME).getTable())
                dfdict = __dataframeToDict(df)
                result = pyfiglet.figlet_format(dfdict['Stock'].split('Stock')[0].strip(), width=os.get_terminal_size()[0])
                print(result)
                print('\n\n')

                priceTable, revenueTable, epsTable, peTable, psTable = __createForecastTables(ticker.upper(), dfdict)

                __printCharts(console, priceTable, revenueTable, epsTable, peTable, psTable)

                # __printDataframe(df)
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
                dfdict = __dataframeToDict(df)

                result = pyfiglet.figlet_format(return_val_stats[1].iloc[0]['Company'].split('Stock')[0].strip(), width=os.get_terminal_size()[0])
                print(result)
                print('\n\n')

                priceTable, revenueTable, epsTable, peTable, psTable = __createForecastTables(ticker.upper(), dfdict)

                __printCharts(console, priceTable, revenueTable, epsTable, peTable, psTable)

                # turn df into table and print it
                # __printDataframe(df)

                end = time.time()
                print("The time of execution of above program is :", (end-start) * 10**3, "ms")
                print()
                print()

                # store the data frames then write a function that translates these dataframs
                sc.setObj(ticker, FILENAME, datadict)