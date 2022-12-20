import requests
from bs4 import BeautifulSoup as bs
from colorama import Fore


__LINK = 'https://finance.yahoo.com/quote/{}/financials?p={}'

__HEADER_TAG = 'D(tbhg)'
__ROWS_TAG = 'D(tbrg)'


def getIncome(ticker):
    url = __LINK.format(str(ticker), str(ticker))
    headers = {"User-Agent":"Mozilla/5.0"}
    data = requests.get(url, headers=headers)
    html = bs(data.text, 'html.parser')
    tagsh = html.find('div', {'class': __HEADER_TAG})
    tagsr = html.find('div', {'class': __ROWS_TAG})
    title = html.find('h1')

    if tagsh == None or len(tagsh) == 0:
        print('Equity ' + ticker + ' not found')
        return
    

    col = []
    for i in range(6):
        col.append(tagsh.contents[0].contents[i].text)
    
    rows = []
    for i in range(len(tagsr.contents)):
        rowsi = []
        for j in range(6):
            rowsi.append(tagsr.contents[i].contents[0].contents[j].text)
        rows.append(rowsi)


    return title.text, col, rows