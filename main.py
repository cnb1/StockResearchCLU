import json
from colorama import Fore

def printMenus(menuList):
    for i in menuList['children']:
        print(Fore.GREEN + i + Fore.WHITE)

if __name__ == "__main__":
    isRun = True
    list = []

    mainfile = open('menus/main.json')
    mainjson = json.load(mainfile)


    while isRun:
        command = input(f"Menu> ")

        if command == "!q":
            isRun = False
        elif command == "ls":
            printMenus(mainjson)
            
        else:
            print(command)