import contextlib
from os import system
from colorama import Fore, Back, Style


system('title Nucleus - Utility [LOG-VIEWER]')
system('cls')

LogTypes = [
    'DEBUG',
    'INFO',
    'WARN',
    'ERROR',
    'FATAL'
]

LogLevel = 2

def PrintLogs():
    with open('nucleus.log', 'r') as Log:
        for LogLine in Log :
            with contextlib.suppress(Exception):
                for HigherLogs in range(5) :
                    if LogLine.startswith(f'[{LogTypes[LogLevel + HigherLogs]}]') :
                        match LogLevel + HigherLogs :
                            case 0 :
                                print(Style.DIM, end='')
                            case 1 :
                                print(Fore.LIGHTCYAN_EX, end='')
                            case 2 :
                                print(Fore.YELLOW, end='')
                            case 3 :
                                print(Fore.RED, end='')
                            case 4 :
                                print(Fore.MAGENTA, end='')
                        print(LogLine, end=f'{Style.RESET_ALL}{Fore.RESET}{Back.RESET}')

                    if LogTypes[LogLevel + HigherLogs] == 'FATAL' :
                        break
    

while True :
    system('cls')
    PrintLogs()
    print(f'Log level {LogTypes[LogLevel]}.')

    LogLevel = input('Enter log level [0 - 4] 0 = DEBUG, 4 = FATAL  >>>')

    try :
        LogLevel = int(LogLevel)
    except Exception :
        print('Invalid input.')
        continue

    if LogLevel < 0 or LogLevel > 4 :
        print('Invalid input.')
        continue