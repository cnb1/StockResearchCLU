import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
from tabulate import tabulate
from colorama import Fore

MIN_FORECAST = 'Min Forecast'
AVG_FORECAST = 'Avg Forecast'
MAX_FORECAST = 'Max Forecast'

A1YF = 'Avg 1 year Forecast'
A2YF = 'Avg 2 year Forecast'
A3YF = 'Avg 3 year Forecast'

dfcol = [MIN_FORECAST, AVG_FORECAST, MAX_FORECAST, 
        A1YF + ' EPS', A2YF + ' EPS', A3YF + ' EPS',
        A1YF + ' Rev', A2YF + ' Rev', A3YF + ' Rev']

def forecastStock(ticker, return_val) :

    url = 'https://www.wallstreetzen.com/stocks/us/nasdaq/' + str(ticker) + '/stock-forecast'

    data = requests.get(url)

    html = bs(data.text, 'html.parser')
    tags = html.find_all('div', {"class": "jss172"})

    if tags == None or len(tags) == 0:
        url = 'https://www.wallstreetzen.com/stocks/us/nyse/' + str(ticker) + '/stock-forecast'
        data = requests.get(url)

        html = bs(data.text, 'html.parser')
        tags = html.find_all('div', {"class": "jss172"})

    if tags == None or len(tags) == 0:
        return


    isRev1 = False
    isRev2 = False
    isRev3 = False

    dfdata = []

    title = html.find('title')


    for tag in tags:
        temp = tag.find_next(string=True)
        tempval = tag.contents[1].find_next(string=True)


        if temp == MIN_FORECAST:
            dfdata.append(tempval)

        elif temp == AVG_FORECAST:
            dfdata.append(tempval)

        elif temp == MAX_FORECAST:
            dfdata.append(tempval)

        elif temp == A1YF:
            if not isRev1 :
                isRev1 = True
                dfdata.append(tempval)
            else:
                dfdata.append(tempval)
                
        elif temp == A2YF:
            if not isRev2 :
                isRev2 = True
                dfdata.append(tempval)
            else:
                dfdata.append(tempval)

        elif temp == A3YF:
            if not isRev3 :
                isRev3 = True
                dfdata.append(tempval)
            else:
                dfdata.append(tempval)


    dict = {}
    for i in range(len(dfcol)):
        dict[dfcol[i]] = [dfdata[i]]
    df = pd.DataFrame(data=dict)
    return_val[0] = df
    # print()
    # print(Fore.LIGHTCYAN_EX + tabulate(df, headers='keys', tablefmt="double_outline") + Fore.WHITE)
    # print()


def generalStats(ticker, return_val):

    url = 'https://www.wallstreetzen.com/stocks/us/nasdaq/' + str(ticker) + '/'

    data = requests.get(url)

    html = bs(data.text, 'html.parser')
    tags = html.find('div', {"class": "MuiContainer-root jss3 MuiContainer-maxWidthXl"})
    title = html.find('h1', {"class": "MuiTypography-root jss109 MuiTypography-h1"})

    if tags == None or len(tags) == 0:
        url = 'https://www.wallstreetzen.com/stocks/us/nyse/' + str(ticker) + '/'
        data = requests.get(url)

        html = bs(data.text, 'html.parser')
        tags = html.find('div', {"class": "MuiContainer-root jss3 MuiContainer-maxWidthXl"})
        title = html.find('h1', {"class": "MuiTypography-root jss109 MuiTypography-h1"})


    if tags == None or len(tags) == 0:
        print('Equity ' + ticker + ' not found')
        return

    dftitle = pd.DataFrame(data={'Company':[title.contents[1]]})

    spansval = tags.findAll('div', {'class':'MuiTypography-root MuiTypography-h4'})
    
    spanstitle = tags.findAll('div', {'class':'MuiTypography-root MuiTypography-h6'})

    dict = {}
    price = ticker.upper() + ' Price'
    rev = 'Revenue'

    for i in range(len(spanstitle)):
        if spanstitle[i].find_next(string=True) == price or spanstitle[i].find_next(string=True) == rev:
            dict[spanstitle[i].find_next(string=True)] = [spansval[i].find_next(string=True)]

    df = pd.DataFrame(data=dict)
    return_val[0] = df
    return_val[1] = dftitle