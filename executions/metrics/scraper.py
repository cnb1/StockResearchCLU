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

def buildTags(tags):

    isRev1 = False
    isRev2 = False
    isRev3 = False
    dfdata = []

    for tag in tags:

        if MIN_FORECAST in tag.text:
            dfdata.append(tag.contents[1].contents[0].contents[0].contents[0].text)
            dfdata.append(tag.contents[1].contents[0].contents[0].contents[1].contents[0].text)


        if AVG_FORECAST in tag.text:
            dfdata.append(tag.contents[1].contents[1].contents[0].contents[0].text)
            dfdata.append(tag.contents[1].contents[1].contents[0].contents[1].contents[0].text)

        if MAX_FORECAST in tag.text:
            dfdata.append(tag.contents[1].contents[2].contents[0].contents[0].text)
            dfdata.append(tag.contents[1].contents[2].contents[0].contents[1].contents[0].text)

        if A1YF in tag.text:
            if not isRev1:
                dfdata.append(tag.contents[1].contents[0].contents[0].contents[0].text + ' EPS')
                dfdata.append(tag.contents[1].contents[0].contents[0].contents[1].contents[0].text)
                isRev1 = True
            else:
                dfdata.append(tag.contents[1].contents[0].contents[0].contents[0].text + ' Rev')
                dfdata.append(tag.contents[1].contents[0].contents[0].contents[1].contents[0].text)


        if A2YF in tag.text:
            if not isRev2:
                dfdata.append(tag.contents[1].contents[1].contents[0].contents[0].text + ' EPS')
                dfdata.append(tag.contents[1].contents[1].contents[0].contents[1].contents[0].text)
                isRev2 = True
            else:
                dfdata.append(tag.contents[1].contents[1].contents[0].contents[0].text + ' Rev')
                dfdata.append(tag.contents[1].contents[1].contents[0].contents[1].contents[0].text)

        if A2YF in tag.text:
            if not isRev3:
                dfdata.append(tag.contents[1].contents[2].contents[0].contents[0].text + ' EPS')
                dfdata.append(tag.contents[1].contents[2].contents[0].contents[1].contents[0].text)
                isRev3 = True
            else:
                dfdata.append(tag.contents[1].contents[2].contents[0].contents[0].text + ' Rev')
                dfdata.append(tag.contents[1].contents[2].contents[0].contents[1].contents[0].text)
            
    return dfdata

    
def forecastStock(ticker, return_val) :

    url = 'https://www.wallstreetzen.com/stocks/us/nasdaq/' + str(ticker) + '/stock-forecast'

    data = requests.get(url)

    html = bs(data.text, 'html.parser')
    tags = html.find_all('div', {"class": "MuiCardContent-root"})

    if tags == None or len(tags) == 0:
        url = 'https://www.wallstreetzen.com/stocks/us/nyse/' + str(ticker) + '/stock-forecast'
        data = requests.get(url)

        html = bs(data.text, 'html.parser')
        tags = html.find_all('div', {"class": "MuiCardContent-root"})

    if tags == None or len(tags) == 0:
        return

    dfdata = buildTags(tags)

    dict = {}
    for i in range(0, len(dfdata), 2):
        dict[dfdata[i]] = [dfdata[i+1]]
        
    df = pd.DataFrame(data=dict)
    # print(Fore.LIGHTCYAN_EX + tabulate(df, headers='keys', tablefmt="double_outline") + Fore.WHITE)
    print()

    return_val[0] = df


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