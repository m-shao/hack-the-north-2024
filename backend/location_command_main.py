from location_interpreter import find_most_similar_room  
from sp_recog import detect_speech
from constants.valid_command_prefixes import valid_command_prefixes
from voiceover import play_audio_pygame

def main():
    play_audio_pygame("Hey, where would you like to go?")
    user_input = detect_speech()
    
    for prefix in valid_command_prefixes:
        if user_input.lower().startswith(prefix):
            user_input = user_input.lower().split(prefix)[1]
            break
    
    most_similar_room = find_most_similar_room(user_input)
    
    play_audio_pygame(f"starting navigation to {most_similar_room}")
    #send this to the frontend to get infomation back
    
    print(most_similar_room)

if __name__ == "__main__":
    main()