from concurrent.futures import thread
import json
import threading
import importlib
from colorama import Fore

import printFunctions as pf

filename = 'filename'

def thread_func(command, menuList):
    print("starting thread")

    tocall = importlib.import_module(menuList[command][filename])
    tocall.stockForecast()

    print("ending thread")

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
                    print("execution found")
                    
                    t = threading.Thread(target=thread_func, args=(command, list[list.__len__()-1]))
                    t.start()
                    t.join()
                    print("exiting if statement")

                else:
                    print(Fore.RED + "Execution not found" + Fore.WHITE)