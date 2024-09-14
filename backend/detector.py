import os
from cv2 import VideoCapture, imshow, imwrite
from openai import OpenAI
import dotenv
import base64
import requests

dotenv.load_dotenv(".env")
openai_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)


def capture_image():
    cam = VideoCapture(0)

    result, image = cam.read()
    if result:
        # saving image in local storage
        imwrite("captured_image.png", image)
    else:
        print("No image detected. Please! try again")


def get_image_text():
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
                                "understand it"
                                "the best."
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


capture_image()
get_image_text()
