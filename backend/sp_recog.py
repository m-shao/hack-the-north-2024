import speech_recognition as sr

r = sr.Recognizer()

"""
Stores audio in file --> user has to continuously speak or else it stops

Really funky as we are using an engine to recognize speech
"""
with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source)
    print("Time over, thanks")

    try:
        # using google speech recognition
        print("Text: " + r.recognize_google(audio_text))
    except:
        print("Sorry, I did not get that.")