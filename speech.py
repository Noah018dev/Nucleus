from pathlib import Path
from openai import OpenAI
from datastore import OpenAI_API_KEY
from currylogger import *

cachever = -1
client = OpenAI(api_key=OpenAI_API_KEY)

def SpeakText(txt : str, voice) -> None :
    global cachever

    cachever += 1
    speech_file_path = Path(__file__).parent / f"{cachever}.mp3"
    response = client.audio.speech.create(
  model="tts-1",
  voice=voice,
  input=txt
  )
    debug(f'Speaking "{txt}" with voice model {voice}')

    response.stream_to_file(speech_file_path)
  
def Transcription(Path) -> None :
  print('Reconizing text...')
  audio_file = open(Path, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
  )
  return transcription.text

