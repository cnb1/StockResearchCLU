from concurrent.futures import thread
import json
import threading
import importlib
from colorama import Fore
from rich.console import Console

import printFunctions as pf
import cache.stockCache as sc
import time

filename = 'filename'


# TODO
# - check to make sure date is working
# - get current eps
# - use termoplot to plot the rev and eps estimates
# - do overall market valuations
# - do rest of financials


# - create feature so that i type dynamic and i can do -f ticker for forecast and -r ticker for ratios 
#   allows me to switch between metrics and any of the rest of the commands each execution has its own unique key


def thread_func(command, menuList):

    tocall = importlib.import_module(menuList[command][filename])
    tocall.run(list)


if __name__ == "__main__":

    console = Console()
    # load persistant cache
    with console.status("[bold green]Loading cache...") as status:
        time.sleep(2)
        isRemoved = sc.load()
    
    if isRemoved:
        sc.save()

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
        elif "-" in command:
            print('super is called')
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