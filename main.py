from concurrent.futures import thread
import json
from re import I
import threading
import importlib
from colorama import Fore
from rich.console import Console
import os
import printFunctions as pf
import cache.stockCache as sc
import time

filename = 'filename'


# TODO
# add the quarterly financials
# fix the issue with the dm fiancials
#


def thread_func(command, menuList):

    tocall = importlib.import_module(menuList[command][filename])
    tocall.run(context)

def __super_func(execution):
    tocall = importlib.import_module(execution)
    tocall.run(context)

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
    context = []

    mainfile = open('menus/main.json')
    mainjson = json.load(mainfile)
    supersdict = {}

    if os.stat('menus/supers.json').st_size != 0:
        supersfile = open('menus/supers.json')
        supersjson = json.load(supersfile)

        for menu in mainjson['menus']:
            tempfile = open('menus/'+menu+'.json')
            tempjson = json.load(tempfile)

            for exec in tempjson['executions']:
                if exec in supersjson:
                    supersdict[supersjson[exec]] = tempjson[exec]['filename']

    context.append(mainjson)

    while isRun:
        
        command = input(Fore.YELLOW + pf.createConsole(context) + Fore.WHITE)

        if command == "!q":
            isRun = False
        elif "-" in command:
            if command in supersdict:
                t = threading.Thread(target=__super_func, args=(supersdict[command],))
                t.start()
                t.join()
            else:
                print(Fore.RED + "Super command not found" + Fore.WHITE)
        elif command == "ls":
            print()
            pf.printMenus(context[context.__len__()-1])
            print()
        elif command == "..":
            context.pop()
        else:
            if pf.checkMenus(context, command, context[context.__len__()-1]) :
                continue
            else :
                if pf.checkExecutions(command, context[context.__len__()-1]):                    
                    t = threading.Thread(target=thread_func, args=(command, context[context.__len__()-1]))
                    t.start()
                    t.join()
                else:
                    print(Fore.RED + "Execution not found" + Fore.WHITE)