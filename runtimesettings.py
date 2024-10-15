from os import system, path, remove
from time import sleep
from currylogger import *
from sys import argv
from utils import IfElse

system('cls')

print('Runtime values are set to default.')

LauncherClient = 'conhost.exe'
Client = 'n-client.exe'
ComspecLaunch = '%comspec% /s /q /d /u /e:off /c'
Python = 'python.exe'
Verbose = 0
AsyncVoice = 'true'

def GetCommand() -> str :
    return f'start runtime-proxy.cmd "{LauncherClient} --headless {ComspecLaunch} start /wait {Client} {Python} -B -q -u {"-v " * Verbose} .\\ai.py --run-program --wipe-logs {IfElse(AsyncVoice.lower() == 'true', '', '--async-voice')}"'

if len(argv) == 1 :
    argv.append(' ')

def AskWithConfirmation(GlobalsKeyName) -> None :
    print(f'\nEditing "{GlobalsKeyName}". Currently set to "{GlobalsKeyName} = {globals()[GlobalsKeyName]}".\nHit enter and it will stay default.\n')
    UserInput = input('>>>')
    if UserInput != '' :
        print('Changed value.')
        globals()[GlobalsKeyName] = UserInput
    else :
        print('Did not change value.')

if argv[1] == '--auto':
    Command = GetCommand()
elif argv[1] == '--advanced':
    AskWithConfirmation('LauncherClient')
    AskWithConfirmation('Client')
    AskWithConfirmation('ComspecLaunch')
    AskWithConfirmation('Python')
    AskWithConfirmation('Verbose')
    AskWithConfirmation('AsyncVoice')

    Verbose = int(Verbose)
    Command = GetCommand()

    print(f'\n\nLaunch command : "{Command}"\n')
    system('pause')

elif input('Do you wish to change them? [Y/N] >>>').lower() == 'y':
    AskWithConfirmation('LauncherClient')
    AskWithConfirmation('Client')
    AskWithConfirmation('ComspecLaunch')
    AskWithConfirmation('Python')
    AskWithConfirmation('Verbose')
    AskWithConfirmation('AsyncVoice')

    Verbose = int(Verbose)
    Command = GetCommand()

    print(f'\n\nLaunch command : "{Command}"\n')
    system('pause')

else:
    Command = GetCommand()
system(Command)
sleep(2)
debug('[RSUI] Made sure logs were set up.')
debug('[RSUI] Launched with arguments :')
debug(Command)

while not(path.exists('aidump.json')) :
    sleep(0.5)

debug('[RSUI] Runtime Settings UI is about to exit.')
remove('aidump.json')
debug('[RSUI] Runtime Settings UI deleted the AIDUMP for the greetings message')
info('[RSUI] Runtime Settings UI terminated.')
quit()
