import speech_recognition as sr

def detect_speech():
    r = sr.Recognizer()

    """
    Stores audio in file --> user has to continuously speak or else it stops

    Really funky as we are using an engine to recognize speech
    """
    with sr.Microphone() as source:
        print("Talk")
        r.adjust_for_ambient_noise(source, duration=1)
        audio_text = r.listen(source)
        print("Time over, thanks")

        try:
            response = r.recognize_google(audio_text)
            # using google speech recognition
            print("Text: " + r.recognize_google(audio_text))
            return response
        except:
            print("Sorry, I did not get that.")
    return "Sorry, I did not get that."

if __name__ == "__main__":
    detect_speech()