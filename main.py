import json
from colorama import Fore

import printFunctions as pf

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
                    # TODO create a new thread here that executes the execution
                else:
                    print(Fore.RED + "Execution not found" + Fore.WHITE)