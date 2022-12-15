from importlib.resources import contents
from string import whitespace
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
from tabulate import tabulate
from colorama import Fore

from rich.console import Console
from time import sleep

def col(x):
    return ['background-color: yellow'] * 4

MIN_FORECAST = 'Min Forecast'
AVG_FORECAST = 'Avg Forecast'
MAX_FORECAST = 'Max Forecast'

A1YF = 'Avg 1 year Forecast'
A2YF = 'Avg 2 year Forecast'
A3YF = 'Avg 3 year Forecast'

dfcol = [MIN_FORECAST, AVG_FORECAST, MAX_FORECAST, 
        A1YF + ' EPS', A2YF + ' EPS', A3YF + ' EPS',
        A1YF + ' Rev', A2YF + ' Rev', A3YF + ' Rev']

def scrap():
        #TODO do a check of nasdaq url or nyse for the url creation
    url = 'https://www.wallstreetzen.com/stocks/us/nasdaq/' + str('aapl') + '/'

    data = requests.get(url)

    html = bs(data.text, 'html.parser')
    tags = html.find('div', {"class": "MuiContainer-root jss3 MuiContainer-maxWidthXl"})
    spansval = tags.findAll('div', {'class':'MuiTypography-root MuiTypography-h4'})
    
    spanstitle = tags.findAll('div', {'class':'MuiTypography-root MuiTypography-h6'})

    title = html.find('h1', {"class": "MuiTypography-root jss109 MuiTypography-h1"})

    print(title.contents[1])
    dftitle = pd.DataFrame(data={'Company':[title.contents[1]]})
    # print(dftitle.to_string(index=False))
    dict = {}

    for i in range(len(spanstitle)):
        dict[spanstitle[i].find_next(string=True)] = [spansval[i].find_next(string=True)]

    df = pd.DataFrame(data=dict)
    ticker = 'aapl'
    print()
    # print(Fore.LIGHTCYAN_EX + tabulate(df, headers='keys', tablefmt="double_outline", showindex=False) + Fore.WHITE)
    print()
    print(dict[ticker.upper() + ' Price'])

    return df, dftitle


if __name__ == '__main__':
    # df, dftitle = scrap()
    # print(dftitle.to_string(index=False))
    # print(Fore.LIGHTCYAN_EX + tabulate(df, headers='keys', tablefmt="double_outline", showindex=False) + Fore.WHITE)
    data = pd.DataFrame({
    "id": [7058],
    "name": ['ramya'],
    "subjects": ['php/js']
    }
    )
    
    # get first row using head() function
    print(data.columns[0])
    print(data.iloc[0].iloc[1])
    print(data)

    for i in range(len(data.columns)):
        print(i)
    
    console = Console()

    data = [1, 2, 3, 4, 5]
    with console.status("[bold green]Fetching data...") as status:
        while data:
            num = data.pop(0)
            sleep(1)
            console.log(f"[green]Finish fetching data[/green] {num}")

        console.log(f'[bold][red]Done!')
