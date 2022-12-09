import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
from tabulate import tabulate

MIN_FORECAST = 'Min Forecast'
AVG_FORECAST = 'Avg Forecast'
MAX_FORECAST = 'Max Forecast'

A1YF = 'Avg 1 year Forecast'
A2YF = 'Avg 2 year Forecast'
A3YF = 'Avg 3 year Forecast'

dfcol = [MIN_FORECAST, AVG_FORECAST, MAX_FORECAST, 
        A1YF + ' EPS', A2YF + ' EPS', A3YF + ' EPS',
        A1YF + ' Rev', A2YF + ' Rev', A3YF + ' Rev']

dfdata = []

def forecast(ticker) :

    url = 'https://www.wallstreetzen.com/stocks/us/nasdaq/' + str(ticker) + '/stock-forecast'

    data = requests.get(url)

    html = bs(data.text, 'html.parser')
    tags = html.find_all('div', {"class": "jss172"})

    isRev1 = False
    isRev2 = False
    isRev3 = False


    for tag in tags:
        # print(tag)
        temp = tag.find_next(string=True)
        tempval = tag.contents[1].find_next(string=True)
        # print('====================================')
        # print('====================================')

        
        # temp = article

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
    print(tabulate(df, headers='keys'))