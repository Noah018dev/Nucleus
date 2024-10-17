import threading, requests, pygame, os
from typing import Callable as function
from speech import SpeakText as SpeakToFile
from currylogger import *



from time import sleep
def GenerateSystemMessage(SetupText : str) -> dict :
    return {"role": "system", "content": SetupText}

def GetPromptIndex(Choices : list, Index : int) -> str :
    return Choices[Index].message.content

def PlayFile(FilePath : str, Async : bool) -> function:
    info(f'Playing file {FilePath}')
    pygame.init()
    pygame.mixer.init()

    # Load the MP3 file
    t1 = threading.Thread(target=pygame.mixer.music.load, args=(FilePath,))
    t1.start()
    t1.join()

    # Play the music
    t2 = threading.Thread(target=pygame.mixer.music.play)
    t2.start()

    # Keep the program running until the music finishes
    t3 = threading.Thread(target=pygame.mixer.music.get_busy)
    t3.start()
    while t3.is_alive():
        sleep(0.3)
        if Async :
            t2.join()
            break

    pygame.mixer.stop()

    return pygame.mixer.stop
    

def DownloadFromURI(URI, SaveToFile) -> None :
    response = requests.get(URI, stream=True)
    
    if response.status_code == 200:
        with open(SaveToFile, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        debug('Downloaded file.')
        print('Downloaded')
    else:
        print(f'Unknown Error {response.status_code}')

def IfElse(Toggle, IfFalse, IfTrue) -> object:
    return IfTrue if Toggle else IfFalse

def SystemMessageConstructor(Prompt) -> dict :
    return {'role' : 'system', 'content' : Prompt}

def SpeakWithOutput(speech: str, Voice, AsyncVoice, cachever, disableasync=False) -> function :

    if Voice == 'none' :
        return

    """
    Speak some text with a given voice and then play the file.
    If disableasync is true, the function will not play the file asynchronously.
    """
    # Check if the file to delete exists
    if cachever > 0:
        file_to_delete = f'{cachever - 10}.mp3'
        if os.path.exists(file_to_delete):
            try:
                os.remove(file_to_delete)
                debug(f'Removed {file_to_delete} to save space.')
            except OSError as e:
                error(f'Error: {e.filename} - {e.strerror}')
    cachever += 1
    while True :
        try :
            SpeakToFile(speech, Voice)
            break
        except PermissionError :
            cachever += 1
            continue
    return PlayFile(f'{cachever}.mp3', AsyncVoice and not(disableasync))