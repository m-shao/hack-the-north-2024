import requests
import json
import os
from secrets import GOOGLE_APPLICATION_CREDENTIALS
import sounddevice as sd
from pydub import AudioSegment
import io
import numpy as np

from google.cloud import texttospeech


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

# Initialize the client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="Hello, world!")

# Build the voice request, select the language code ("en-US") and the voice name
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Studio-O")

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

raw_audio = np.frombuffer(response.audio_content, dtype=np.int16)

sample_rate = 24000  # Default sample rate for LINEAR16 in Google TTS
sd.play(raw_audio, samplerate=sample_rate, blocking=True)