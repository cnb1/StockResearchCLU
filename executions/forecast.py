import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import scraper


#TODO get this import to work
def stockForecast():
    print("stock forecast")
    #TODO: create the python web scrapper for the zacks information
    # input stock
    ticker = input()
    scraper.forecast(ticker)