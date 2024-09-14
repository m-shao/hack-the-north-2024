import os
from secrets import GOOGLE_APPLICATION_CREDENTIALS
import io
import pygame
from google.cloud import texttospeech
import threading

def text_to_speech(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

    # Initialize the client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the voice name
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Studio-O"
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    return response

def play_audio(audio_content):
    
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 data into a pygame Sound object from memory
    pygame.mixer.music.load(io.BytesIO(audio_content))

    # Play the sound
    pygame.mixer.music.play()    

    # Keep the program running until the sound finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":    
    response = text_to_speech("Hello, world!")
        
    audio_thread = threading.Thread(target=play_audio, args=(response.audio_content,))
    audio_thread.start()