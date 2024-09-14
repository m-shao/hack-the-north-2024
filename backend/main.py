import os
from cv2 import VideoCapture, imwrite, waitKey
from openai import OpenAI
import dotenv
import base64
import requests
import speech_recognition as sr
import threading
import keyboard
import requests
import json
import os
from secrets import GOOGLE_APPLICATION_CREDENTIALS
import sounddevice as sd
from pydub import AudioSegment
import io
from playsound import playsound
from google.cloud import texttospeech
import threading
from pynput.keyboard import Key, Listener

dotenv.load_dotenv(".env")
openai_key = os.environ.get("OPENAI_API_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS
client = OpenAI(api_key=openai_key)


def periodic_detector():
    cam = VideoCapture(0)

    result, image = cam.read()
    if result:
        imwrite("captured_image.png", image)
    else:
        print("No image detected. Please! try again")

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    image_path = "captured_image.png"  # 728 x 410: gpt-4o-mini --> 4 secs
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_key}"
    }

    # gpt-4o-mini --> 14 secs
    # gpt-4-turbo --> 14 secs
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system",
             "content": "You are designed to help describe the environments around a visually impaired person."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I am a visually impaired person, describe the image to me in a way to help me better "
                                "understand it. 1-2 sentences, describe where key objects (such as persons) are."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())


def get_input():
    r = sr.Recognizer()

    mic_error = False
    with sr.Microphone() as source:
        print("Talk")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio_text = r.listen(source)
        print("Time over, thanks")

        try:

            user_output = r.recognize_google(audio_text)
        except:
            mic_error = True
    print("asdasd")
    if not mic_error:
        return user_output
    else:
        return mic_error


def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Studio-O"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return response


def use_helper(text):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a tutor who takes a textbook and summarizes it in 50 words",
            },
            {"role": "user", "content": text},
        ],
    )

    return completion.choices[0].message.content


while True:
    def on_press(key):
        print('{0} pressed'.format(
            key))


    def on_release(key):
        print('{0} release'.format(
            key))
        if key == Key.esc:
            # Stop listener
            return False
        if key == Key.space:
            print("starting audio")
            user_output = get_input()
            print("asd")
            if not user_output:
                playsound("audio_not_found.mp3")
            else:
                with open("output.mp3", "wb") as out:
                    out.write(text_to_speech(use_helper(user_output)).audio_content)
                playsound('output.mp3')


    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    # if keyboard.is_pressed('esc'):
    #     print("Loop terminated by user.")
    #     break

