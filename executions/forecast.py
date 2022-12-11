import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import scraper


def stockForecast():
    # TODO create looping for this inputs
    print(list)

    isRun = True
    while isRun:
        ticker = input()
        print('ticker is: ' + ticker)
        if ticker == "!q":
            isRun = False
        else:
            scraper.forecast(ticker)

        print()