from concurrent.futures import thread
import json
import threading
import importlib
from colorama import Fore

import printFunctions as pf

filename = 'filename'


# TODO 
# - make scraper better for forecast for tag MuiCardContent-root
# - do financials

# - reduce the top DF to only have price eps and rev
# - create feature so that i type dynamic and i can do -f ticker for forecast and -r ticker for ratios 
#   allows me to switch between metrics and any of the rest of the commands each execution has its own unique key
# - add financials feature
# - add view stock chart feature
# - create all in one report feature 
# - add other features for forecast visualizations
# - background thread that loads all last 7 days requested items and eliminates past
#   7 days items. uses these items to reduce requests made


def thread_func(command, menuList):

    tocall = importlib.import_module(menuList[command][filename])
    tocall.run(list)


if __name__ == "__main__":

    pf.printName()

    isRun = True
    list = []

    mainfile = open('menus/main.json')
    mainjson = json.load(mainfile)

    list.append(mainjson)

    while isRun:
        
        command = input(Fore.YELLOW + pf.createConsole(list) + Fore.WHITE)

        if command == "!q":
            isRun = False
        elif command == "ls":
            print()
            pf.printMenus(list[list.__len__()-1])
            print()
        elif command == "..":
            list.pop()
        else:
            if pf.checkMenus(list, command, list[list.__len__()-1]) :
                continue
            else :
                if pf.checkExecutions(command, list[list.__len__()-1]):                    
                    t = threading.Thread(target=thread_func, args=(command, list[list.__len__()-1]))
                    t.start()
                    t.join()
                else:
                    print(Fore.RED + "Execution not found" + Fore.WHITE)