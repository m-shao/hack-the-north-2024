import os
from cv2 import VideoCapture, imwrite
from openai import OpenAI
import dotenv
import base64
import requests
import speech_recognition as sr
import threading
import keyboard

dotenv.load_dotenv(".env")
openai_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)
r = sr.Recognizer()


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
    mic_error = False
    with sr.Microphone() as source:
        audio_text = r.listen(source)

        try:
            user_output = r.recognize_google(audio_text)
        except:
            mic_error = True
    if not mic_error:
        return user_output
    else:
        return mic_error


while True:
    # periodic_detector()
    if keyboard.is_pressed('esc'):
        print("Loop terminated by user.")
        break
    if keyboard.is_pressed('t'):
        # PLAY AUDIO SIMILAR TO SIRI
        print("starting audio")
        user_output = get_input()
        if not user_output:


