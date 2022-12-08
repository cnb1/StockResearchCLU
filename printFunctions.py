from colorama import Fore
import json

menus = "menus"
executions = "executions"

def printName():
    print("""

    |||| EQUITY TERMINAL ||||

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

def createConsole(list):
    
    consoleout = ""

    for i in list:
        consoleout += '/' + i['name']

    return consoleout + ' > '
