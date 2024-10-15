import pygame
import requests
from typing import Callable as function
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
    pygame.mixer.music.load(FilePath)

    # Play the music
    pygame.mixer.music.play()

    # Keep the program running until the music finishes
    try:
        while pygame.mixer.music.get_busy():
            sleep(0.3)

            if Async :
                break
    except Exception :
        pygame.mixer.stop()

    return pygame.mixer.stop
    


def DownloadFromURI(URI, SaveToFile) -> None :
    response = requests.get(URI)
    
    if response.status_code == 200:
        with open(SaveToFile, 'wb') as file:
            file.write(response.content)
        debug('Downloaded file.')
        print('Downloaded')
    else:
        print(f'Unknown Error {response.status_code}')

def IfElse(Toggle, IfFalse, IfTrue) -> object:
    return IfTrue if Toggle else IfFalse