import io
from pydub import AudioSegment
from google.cloud import speech

def transcribe_audio(file_path):
    client = speech.SpeechClient()

    # Load the audio into memory
    audio_segment = AudioSegment.from_file(file_path)
    audio_content = audio_segment.export(format='wav')

    with io.BytesIO(audio_content.read()) as audio_file:
        audio_data = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_data)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response.results[0].alternatives[0].transcript if response.results else ""

# Call your function
# Make sure to replace 'audio.wav' with the path of your audio file
transcript = transcribe_audio('audio.wav')
print(transcript)
