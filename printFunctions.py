from colorama import Fore
import json
from rich.console import Console
from rich.table import Table

menus = "menus"
executions = "executions"
SCALE_VAL = 10
BAR_LEN = 12
BAR_TOKEN = '■'
BAR_ROW = BAR_TOKEN * BAR_LEN
TABLE_WIDTH = 100

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

def createChart(title, labels, values):
    maxval = max(values)
    minval = min(values)
    
    scale = (maxval - minval) / SCALE_VAL
    totals = []

    for i in values:
        totals.append(int(round((i-minval)/scale)))

    lambdafunction = lambda x : ((lambda: x, lambda: ' ')[x==' '], lambda: '#')[x=='#']()
    listlambda = []

    listlambda.append([str(round(minval, 2)), BAR_ROW, BAR_ROW, BAR_ROW, BAR_ROW])
    # minval = minval - scale
    for i in range(SCALE_VAL):
        ltemp=[]
        ltemp.append(str(round(minval + scale, 2)))
        minval = minval + scale
        for j in range(len(totals)):
            if totals[j] != 0:
                ltemp.append(BAR_ROW)
                totals[j] = totals[j]-1
            else:
                ltemp.append(' ')
        listlambda.insert(0,ltemp)

    table = Table(title=title, show_header=False, show_footer=True, show_edge=False, width=TABLE_WIDTH,
                    title_style='bright_red')
    table.add_column(footer='Amount', style='bright_green')
    for i in labels:
        table.add_column(footer=i, style='bright_blue')

    for i in listlambda:
        x = list(map(lambdafunction, i))
        table.add_row(*x)
    
    return table

    

# if __name__ == '__main__':
#     print(int(round(4.3)))
#     printGraph(['a', 'b', 'c', 'd'],[1.5,2,3, 3.75])