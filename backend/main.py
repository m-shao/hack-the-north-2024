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
from secrets1 import GOOGLE_APPLICATION_CREDENTIALS
import sounddevice as sd
from pydub import AudioSegment
import io
from playsound import playsound
from google.cloud import texttospeech
import threading
from pynput.keyboard import Key, Listener
from location_interpreter import find_most_similar_room
from sp_recog import detect_speech
from constants.valid_command_prefixes import valid_command_prefixes
from voiceover import play_audio_pygame


dotenv.load_dotenv(".env")
openai_key = os.environ.get("OPENAI_API_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS
client = OpenAI(api_key=openai_key)


def periodic_detector(text):
    print("this is running")
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
             "content": "You are designed to help describe the environments around a visually impaired person. I am a visually impaired person, describe the image to me in a way to help me better understand it. 1-2 short sentences, keep it concise, describe where key objects (such as persons) are."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{text}"
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

    # print(response.json())
    with open("output.mp3", "wb") as out:
        out.write(text_to_speech(response.json()['choices'][0]['message']['content']).audio_content)
    playsound('output.mp3')


def get_input():
    playsound("startup.wav")
    while True:
        r = sr.Recognizer()

        mic_error = False
        with sr.Microphone() as source:
            print("Receiving input.")
            r.adjust_for_ambient_noise(source, 1)
            audio_text = r.listen(source)
            print("Input received.")

            try:
                user_output = r.recognize_google(audio_text)
            except:
                mic_error = True
        if not mic_error:
            print("user input: ", user_output)

            user_output = user_output.lower()
            if "hello" in user_output and "world" in user_output:
                room = False

                for prefix in valid_command_prefixes:
                    if prefix in user_output.lower():
                        user_output = user_output.lower().split(prefix)[1]
                        room = True
                        break
                if room:
                    most_similar_room = find_most_similar_room(user_output)
                    print(most_similar_room)
                    play_audio_pygame(f"Starting navigation to {most_similar_room}")
                else:
                    periodic_detector(user_output)
                # with open("output.mp3", "wb") as out:
                #     out.write(text_to_speech(use_helper(user_output)).audio_content)
                # playsound('output.mp3')
        else:
            pass


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



while True:
    # periodic_detector()
    # t2 = threading.Thread(periodic_detector(), args=())

    t1 = threading.Thread(get_input(), args=(), daemon=True)
    t1.start()

    t1.join()

    # periodic_detector()

    # def on_press(key):
    #     print('{0} pressed'.format(
    #         key))

    # def on_release(key):
    #     print('{0} release'.format(
    #         key))
    #     if key == Key.esc:
    #         # Stop listener
    #         return False
    #     if key == Key.space:
    #         print("starting audio")
    #         user_output = get_input()
    #         print("asd")
    #         if not user_output:
    #             playsound("audio_not_found.mp3")
    #         else:
    #             with open("output.mp3", "wb") as out:
    #                 out.write(text_to_speech(use_helper(user_output)).audio_content)
    #             playsound('output.mp3')

    # with Listener(
    #         on_press=on_press,
    #         on_release=on_release) as listener:
    #     listener.join()
