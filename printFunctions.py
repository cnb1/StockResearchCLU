from colorama import Fore
import json

menus = "menus"
executions = "executions"

def printName():
    print("""
 ______    _____    _    _  ________   ________  ___  __     ________   ______    ___     _       _    ________    _    _              _      
|   ___|  |  __ |  | |  || |__   ___| |___   __| \  \/ /    |___   __| |   ___|  |  _\   | \     / |  |__   ___|  | \  | |     /\     | |     
|  |____  | |  ||  | |  ||    |  |        | |     \   /         | |    |  |____  | |/ )  |  \   /  |     |  |     |  \ | |    /  \    | |     
|   ____| | |  ||  | |  ||    |  |        | |      \ /          | |    |   ____| |   /   | \ \ / / |     |  |     | \ \| |   / /\ \   | |     
|  |___   | |__\ \ | |__||  __|  |__      | |      | |          | |    |  |___   | ||\   |  \ V /  |   __|  |__   |  \   |  / /__\ \  | |____ 
|______|  |_____\_\|_____| |________|     |_|      |_|          |_|    |______|  |_||_\  |__|\_/|__|  |________|  |__|\__| /_/    \_\ |______|

    """)

def printMenus(menuList):
    if menus in menuList:
        print("MENUS")
        for i in menuList[menus]:
            print("   " + Fore.GREEN + i + Fore.WHITE)
    
    if executions in menuList:
        print("EXECUTIONS")
        for i in menuList[executions]:
            print("   " + Fore.BLUE + i + Fore.WHITE)



def checkMenus(list, command, menuList):
    if menus in menuList:
        for i in menuList[menus]:
            if command == i:
                # append a new menu to the list
                # load new menu
                file = "menus/" + command + ".json"
                tempfile = open(file)
                tempjson = json.load(tempfile)
                list.append(tempjson)
                return True

    return False

def checkExecutions(command, menuList):
    if executions in menuList:
        for i in menuList[executions]:
            if command == i:
                return True

    return False

def createConsole(list, added = None):
    
    consoleout = ""

    for i in list:
        consoleout += '/' + i['name']

    if added is None:
        return consoleout + ' > '
    else:
        return consoleout + '/' + added + ' > '