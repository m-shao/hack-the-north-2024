from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

from constants.roomslist import rooms as room_names

def find_most_similar_room(user_input):
    # Combine the user input with the room names
    all_texts = [user_input] + room_names
    
    # Initialize the TF-IDF Vectorizer
    vectorizer = TfidfVectorizer().fit_transform(all_texts)
    
    # Calculate the cosine similarity matrix
    cosine_similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:])
    
    # Find the index of the most similar room
    most_similar_index = cosine_similarities.argmax()
    
    return room_names[most_similar_index]

if __name__ == "__main__":
    # Example usage
    user_input="judging l"

    most_similar_room = find_most_similar_room(user_input, rooms)
    print(f"The most similar room to '{user_input}' is '{most_similar_room}'.")