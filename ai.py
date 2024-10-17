import contextlib
from time import sleep, time
from sys import argv
from colorama import Fore, Back
from typing import Callable as function
from json import dump, load
from currylogger import *
import os

AsyncVoice = False

if '--wipe-logs' in argv :
    with open('nucleus.log', 'w') as WipeIt :
        WipeIt.write('Logging started.\n\n')

if '--async-voice' in argv :
    AsyncVoice = True
    info('Async voice mode on.')
else :
    info('Async voice mode off.')




info(f'Launched with arguments "{str(argv)}"')

NoDelete = ''

def delete_mp3_files(directory):
    global NoDelete
    BytesSaved = 0

    for filename in (fn for fn in os.listdir(directory) if fn.endswith(".mp3")):
        file_path = os.path.join(directory, filename)
        try:
            BytesSaved += os.path.getsize(file_path)
            os.remove(file_path)
            debug(f'Deleted file {file_path} while deleting audio caches.')
            if '--silent' not in argv:
                print(f"Deleted: {file_path}, saved {BytesSaved} bytes.")
        except Exception as e:
            warn(e)
            warn(f'Could not delete file {file_path}.')
            NoDelete = file_path

    info(f'delete_mp3_files saved {BytesSaved} bytes.')
    return BytesSaved


def NukeProgram() -> None:
    info('Started cleaning up the program.')
    os.system('title Nucleus - Exiting Application')
    bytes_saved = 0

    # Delete debug dump files
    with contextlib.suppress(Exception):
        bytes_saved += os.path.getsize('aidump.json')
        os.remove('aidump.json')
    # Delete speech caches
    bytes_saved += delete_mp3_files('.')


    # Wipe AI image workshop
    with contextlib.suppress(Exception):
        os.system('conhost cmd /c deletewsp.cmd ')
    print(f'Saved {round(bytes_saved / 1000)}kB.\nPress any key to close this window.')
    os.system('title Nucleus - Cleaning Complete')
    if '--silent' not in argv:
        os.system('pause>nul')
    if NoDelete != '' :
        warn(f'Calling deletez with {NoDelete} to remove..')
        os.system(f'start n-client.exe cmd /c deletez.cmd {NoDelete}')
    os.system(f'taskkill /F /PID {os.getpid()} /T')
    quit()

def PipInstall(Package : str) -> None :
    os.system(f'python -m pip install {Package}')

ArgumentsMatched = False
HelpMessage = '''Nucleus
Options :
    --help                        : Display this help message
    --setup-api-key               : Change or configure your API key for Open AI
    --pip-install-requirements    : Install requirements
    --finish-cleanup              : Cleans all files that are cleaned on exit in case of a crash.
'''
Requirements = ['colorama', 'flask', 'openai', 'python-vlc', 'requests', 'pygame', 'pytz', 'tzlocal']

def SetArgs() -> None :
    global ArgumentsMatched

    ArgumentsMatched = False

for _ in range(15) :
    argv.append('')

if argv[1] == '' :
    print(HelpMessage)
    quit()

match argv[1] :
    case '--help' :
        SetArgs()
        print(HelpMessage)
        quit()

if argv[1] == '--pip-install-requirements' :
    SetArgs()
    if argv[2] == '--auto-upgrade-pip' :
        PipInstall('--upgrade pip --no-warn-script-location')

    for PackageToInstall in Requirements :
        PipInstall(PackageToInstall)
    
    quit()

if argv[1] == '--run-program' :
    ArgumentsMatched = True
    os.system('title Nucleus - Config & cls')

if argv[1] == '--finish-cleanup' :
    ArgumentsMatched = True
    NukeProgram()
    quit()

if not ArgumentsMatched :
    print('Use "--help" for arguments to use with this command.')
    quit()

sleep(1)

os.system('title Nucleus - Config & cls')



from utils import PlayFile, SpeakWithOutput, SystemMessageConstructor
from random import randint


cachever = -1

from charactersmgr import SystemMessages


CharacterNames = list(SystemMessages.keys())
AllVoices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', 'none']
os.system('cls')
print('Choose a voice for your Chatacter...\n')
TMP1 = -1
TMP2 = False
for VoiceName in AllVoices :
    TMP1 += 1
    print(f'#{TMP1 + 1} : {VoiceName.title()}')
    if TMP2 :
        continue
    try :
        SpeakWithOutput(f'Hello, I am {AllVoices[TMP1]}.', AllVoices[TMP1], AsyncVoice, cachever)
    except KeyboardInterrupt :
        TMP2 = True
print('\n')
SelectedVoice = '[Unknown]'
try :
    SelectedVoice = int(input('Voice # : ')) - 1
except BaseException as e :
    error(str(e))
    fatal(f'Selected voice was not int or in range. SV : {SelectedVoice}')


from tzlocal import get_localzone
Max = 10
Current = 0

info(f'Chose voice "{SelectedVoice}".')

while True:
    os.system('cls')
    print('Choose your chatacter...\n')
    while True:
        try :
            Character = list(SystemMessages.keys())[Current]
        except Exception:
            print('No more characters. Looping back to start.')
            Max = 0
            Current = 0
            break
        Current += 1
        print(f'#{SystemMessages[Character]["#"]} : {Character}\n\t{SystemMessages[Character]["Description"]}\n')
        if Current == Max :
            print('\nHit enter to list the next ten characters...')
            break

    TMP1 = input('Chosen Character # >>>')
    if TMP1 == '':
        Max += 10
    else:
        try:
            TMP1 = int(TMP1)
            break
        except Exception :
            print('Not a number.')

TMP2 = CharacterNames[TMP1 - 1]
ChosenSystemMessage = SystemMessages[TMP2]
SystemName = list(SystemMessages.keys())[TMP1 - 1]
Exiting = False

if ChosenSystemMessage['Content'] == 'custom' :
    CustomName = input('Using Custom. Type the name for your AI >>>')
    if CustomName == '!admin' :
        print('Admin character mode activated.')
        ChosenSystemMessage['Content'] = SystemMessageConstructor(f'Your name is {CustomName}. {input("[Content] : ")}')
        ChosenSystemMessage['Description'] = SystemMessageConstructor(f'Your name is {CustomName}. {input("[Description] : ")}')
        CustomName = SystemMessageConstructor(f'Your name is {CustomName}. {input("[TMP2] : ")}')
    else :
        ChosenSystemMessage['Content'] = SystemMessageConstructor(f'Your name is {CustomName}. {input("Using Custom. Type the description for your AI, like how they talk and and interact >>>")}')
        ChosenSystemMessage['Description'] = ChosenSystemMessage['Content']
os.system('title Nucleus')

try :
    os.mkdir('C:\\Nucleus\\')
except FileExistsError :
    ...

from datastore import OpenAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OpenAI_API_KEY)

OutputForms = {
    1 : 'mini',
    2 : 'short',
    3 : 'content',
    4 : 'long',
    5 : 'extra_long'
}

from imagegen import GenerateImage
from serpersearch import SearchWeb, SearchTypes
from datetime import datetime
from datastore import DefaultSystemAI
import threading

os.system('cls')

ShowEncodeMessage = True
SelectedOutputForm = OutputForms[3]

def WaitWithExitAndTitle(Time : int, TitleCycle : int) -> None:
    Start = time()
    while time() - Start < Time and not Exiting:
        sleep(0.01)
        if TitleCycle == 1 :
            os.system(f'title Nucleus - Powered by GPT-4o, your SystemAI ({threading.active_count()})')
        elif TitleCycle == 2 :
            with contextlib.suppress(Exception):
                if TypeOfOutput == 'text':
                    os.system(f'title Nucleus - {SystemName} ({threading.active_count()})')
                elif Output is not None and OutputForms is not None:
                    os.system(f'title Nucleus - {Output[OutputForms[1]]} ({threading.active_count()})')
    if Exiting:
        NukeProgram()

 
def TitleCycle() -> None:
    while True:
        WaitWithExitAndTitle(4, 1)
        WaitWithExitAndTitle(4, 2)
        

        


def GetContent(choices : list, index : int) -> str :
    return choices[index].message.content    

def ListToString(List : list, Seperator : str) -> str :
    OutputString = ''
    
    for Joiner in List :
        OutputString + Joiner + Seperator
    
    return OutputString

ExpectedKeys = ['content', 'exit', 'mini', 'short', 'long', 'extra_long', 'psh', 'img', 'imgprompt', 'query', 'qsources', 'weblnk', 'stype']


thr = threading.Thread(target=TitleCycle, args=(), kwargs={})
thr.start()
debug('Started TitleCycle thead with args () and kwarges {}.')
History = [None]

try :
    print(f'Loaded Chatacter Profile "{CustomName}"')
except :
    print(f'Loaded Chatacter Profile "{SystemName}"')
debug(f'User chose charater "{SystemName}"')
info(f'Loaded Chatacter Profile "{SystemName}"')
ForceUserToSay = 'Greet Me'

if TMP2 == 'Custom' :
    print('Type "!save" to save your custom chatacter')
    print('(Actually it just crashes it right now, don\'t!)')
else :
    print(f'Say hello to {TMP2}!')

while True :
    if ChosenSystemMessage['Content'] == 'default.ai.object' :
        History[0] = DefaultSystemAI(SelectedOutputForm, SearchTypes)
        TypeOfOutput = "json_object"
    else :
        History[0] = ChosenSystemMessage['Content']
        TypeOfOutput = "text"
    try :
        if ForceUserToSay == '' :
            Prompt = input('>>>')
            info(f'[USER] {Prompt}')
        else :
            info(f'Forced user to say "{ForceUserToSay}".')
            Prompt = ForceUserToSay
            ForceUserToSay = ''
    except :
        break

    try :
        if Prompt[0] == '!' :
            match Prompt[1:].split(' ')[0].lower() :
                case 'save' :
                    if TMP2 == 'Custom' :
                        info('Trying to save character...')
                        print(f'Saving character {CustomName}...')
                        with open('customs.json', 'r') as CharListRaw :
                            try :
                                CustomCharacters : list = load(CharListRaw)
                            except BaseException as e :
                                fatal(e)
                                print('Could not save your character!')
                                error('Could not load customs.json.')
                        with open('customs.json', 'w') as Saver :
                            CustomCharacters.append(
                                f'''{
                                    CustomName : {
            "#" : len(SystemMessages) + 1,
            "Content" : ChosenSystemMessage['Content'],
            "Description" : ChosenSystemMessage['Description']
        }
                                }'''
                            )
                            
                            try :
                                dump(CustomCharacters, Saver)
                            except BaseException as e :
                                fatal(e)
                                print('Could not save your character!')
                                
                                error('Could not dump customs.json')
                    else :
                        print('Not using custom character!')
    except IndexError :
        continue

                    


    if Prompt.removeprefix('//') == Prompt :
        History.append({'role' : 'user', 'content' : Prompt})
        try :
            completion = client.chat.completions.create(
                response_format={ "type": TypeOfOutput},
                model = 'gpt-4o',
                messages = History
            )
        except :
            History[0] = SystemMessageConstructor(History[0])
            completion = client.chat.completions.create(
                response_format={ "type": TypeOfOutput},
                model = 'gpt-4o',
                messages = History
            )
        Responses = completion.choices

        if TypeOfOutput == 'json_object' :
            Output : dict = eval(GetContent(Responses, 0))
        else :
            Output : str = GetContent(Responses, 0)

        if TypeOfOutput == 'text' :
            Output = {'content' : Output}

        for LookingForKey in ExpectedKeys :
            if LookingForKey in Output.keys() :
                ...
            else :
                Output[LookingForKey] = ''
                debug(f'Missing key {LookingForKey}. Replacing with nil.')

        debug(f'[RAWBOT] {str(Output)}')

        StaggeredOutput = Output[SelectedOutputForm]
        info(f'[BOT] {StaggeredOutput}')
        LastOneStar = False
        TickCount = 0
        NewChar = ''
        FormattedOutput = ''
        InBold = False
        InCode = False
        for Char in StaggeredOutput :
            if Char == '*' :
                if LastOneStar :
                    LastOneStar = False
                    if InBold :
                        InBold = False
                        NewChar = f'{Back.BLACK}{Fore.WHITE}'
                    else :
                        NewChar = f'{Back.WHITE}{Fore.BLACK}'
                        InBold = True
                    
                else :
                    NewChar = ''
                    LastOneStar = True
            elif Char == '`' :
                if TickCount == 3 :
                    if InCode :
                        InCode = False
                        NewChar = Fore.RESET
                    else :
                        InCode = True
                        NewChar = Fore.MAGENTA
                else :
                    TickCount += 1
                    NewChar = ''
            else :
                TickCount = 0
                LastOneStar = False
                NewChar = Char
            FormattedOutput = FormattedOutput + NewChar

        for Token in FormattedOutput.split(' ') :
            print(Token, end=' ')
            sleep(0.01)
        print('\n')
        try :
            try :
                if Output[SelectedOutputForm] == '' :
                    ...
                else :
                    if AsyncVoice :
                        try :
                            print('\n')
                            while NewVoice.is_alive() :
                                try :
                                    print('\r|', end='')
                                    sleep(0.1)
                                    print('\r/', end='')
                                    sleep(0.1)
                                    print('\r-', end='')
                                    sleep(0.1)
                                    print('\r\\', end='')
                                    sleep(0.1)
                                except :
                                    continue

                            print('\r ')
                        except :
                            ...
                        NewVoice = threading.Thread(target=SpeakWithOutput,args=(Output[SelectedOutputForm], AllVoices[SelectedVoice], AsyncVoice, cachever), kwargs={'disableasync':True})
                        NewVoice.start()
                        
                    else :
                        StopHandle = SpeakWithOutput(Output[SelectedOutputForm], AllVoices[SelectedVoice])
            except BaseException as e :
                error(e)
                fatal('Likely cause, the voice was not in range. You might\'ve seen the range error when selecting the voices above.')
                Exiting = True
                debug('Set program exiting flag to (True)')
                quit()
        except KeyboardInterrupt :
            StopHandle()
            SpeakWithOutput('', 'echo', True, cachever)
            debug('Made the voice engine shut up.')


        if Output['exit'] == 1 :
            if input('\nExit? [Y/N]').lower() == 'y' :
                info('Validly raised the exit flag.')
                Exiting = True
                break
            

        with open('aidump.json', 'w') as JSONDump :
            try :
                JSONDump.write(str(Output))
                debug('Successfully wrote the raw json dump of the API response to "aidump.json".')
            except UnicodeEncodeError :
                if ShowEncodeMessage :
                    warn('Encode error. Disabling further encode warnings.')
                    print('Could not encode. You can keep chatting but dump doesn\'t work so it may crash at any time. Proceed with caution.')
                    ShowEncodeMessage = False

        if Output['img'] == 1 :
            try :
                debug('Deleting rimage.png')
                os.remove('C:\\Nucleus\\rimage.png')
            except :
                ...
            info(f'Generating image with prompt {Output["imgprompt"]}.')
            GenerateImage(Output['imgprompt'], 'C:\\Nucleus\\rimage.png')

        try :
            os.system(Output['psh'])
        except :
            ...

        if Output['query'] != '' :
            History.append({'role' : 'system', 'content' : 'The next system message is the raw JSON content of your search.'})
            debug(f'Googling {Output["query"]}')
            try :
                History.append({'role' : 'system', 'content' : str(SearchWeb(Output['query'], Output['stype']))})
            except :
                print('Failed using the API. Using search.')
                History.append({'role' : 'system', 'content' : str(SearchWeb(Output['query'], 'search'))})
            debug(f'SerperAPI responded.')
            ForceUserToSay = '\n'
        
        if Output['qsources'] != '' :
            debug('Listing sources.')
            print('Sources :')
            try :
                SN = 0
                for Source in Output['qsources'] :
                    SN += 1
                    print(f'[{SN}]\t {Source}') 
            except :
                print(Output['qsources'])   
        
        if Output['weblnk'] != '' :
            info(f'Opening web page {Output["weblnk"]}')  
            os.system(f'explorer {Output["weblnk"]}')

    else :
        Command = Prompt.removeprefix('//').split(' ')
        match Command[0] :
            case 'out' :
                try :
                    SelectedOutputForm = OutputForms[int(Command[1])]
                except ValueError :
                    print('MUST BE INT 1-5')
                except KeyError :
                    print('INT WAS OUT OF RANGE')

            

print('\n')
Exiting = True