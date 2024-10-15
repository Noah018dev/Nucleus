from openai import OpenAI
from datastore import OpenAI_API_KEY
from utils import DownloadFromURI
from currylogger import *
client = OpenAI(api_key=OpenAI_API_KEY)

def GenerateImage(Prompt, SaveToFile) -> None :
    print('\nGenerating Image...')
    response = client.images.generate(
  model="dall-e-3",
  prompt=Prompt,
  size="1024x1024",
  quality="standard",
  n=1,
)
    print('Generated Successfully.')
    ImageURI = response.data[0].url
    info(f'Image generated "{Prompt}" available at {ImageURI}.')
    DownloadFromURI(ImageURI, SaveToFile)
    print('\n')
    debug('Downloaded image.')