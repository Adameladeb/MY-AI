import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pyttsx3
import wikipedia
import datetime
import webbrowser
import random
import spotipy
import spotipy.util as util
import random
import requests

class YourAssistant:

    # Initialize NewsAPI key
    NEWS_API_KEY = "your_news_api_key"

class YourAssistant:

    # Initialize Spotify client ID and secret
    CLIENT_ID = "your_client_id"
    CLIENT_SECRET = "your_client_secret"

    def __init__(self):
        # Initialize Spotify token
        self.token = util.prompt_for_user_token(
            "your_username",
            scope="user-library-read user-modify-playback-state",
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            redirect_uri="http://localhost:8888/callback/"
        )
        # Initialize Spotify client
        self.sp = spotipy.Spotify(auth=self.token)

class Assistant:
    def __init__(self):
        self.name = 'urname'
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.user = None
        self.preferences = None

    def listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None

    def process_command(self, command):
        tokens = word_tokenize(command)
        tokens = [word.lower() for word in tokens if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if not word in stop_words]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        return tokens

    def respond(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def greet(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            self.respond(f"Good morning, {self.user}. How can I assist you?")
        elif 12 <= hour < 18:
            self.respond(f"Good afternoon, {self.user}. How can I assist you?")
        else:
            self.respond(f"Good evening, {self.user}. How can I assist you?")

    def get_user(self):
        self.respond("May I know your name?")
        self.user = self.listen()
        self.respond(f"Nice to meet you, {self.user}")

    def get_preference(self):
    self.respond("What type of music do you like?")
    music_genres = ["rock", "pop", "hip hop", "classical", "jazz", "rap","lofi"]
    while True:
        user_input = self.listen()
        if user_input is not None:
            tokens = self.process_command(user_input)
            for token in tokens:
                if token in music_genres:
                    self.preferences = {"music_genre": token}
                    self.respond(f"Great, I'll remember that you like {token} music!")
                    return
            self.respond("I'm sorry, I didn't understand. Please choose from the following genres: rock, pop, hip hop, classical, jazz.")

This code will prompt the user to enter their preferred music genre, and will only recognize a preference if it matches one of the preset options in the music_genres list. If the user enters a recognized genre, the preference is saved as a dictionary in the self.preferences attribute, and the assistant confirms the preference to the user. If the user's input doesn't match any recognized genres, the assistant will ask the user to choose from the preset options again.

    def play_music(self, genre):

        if self.token:
            # Search for tracks of the specified genre
            results = self.sp.search(q=f"genre:{genre}", type="track")
            tracks = results['tracks']['items']

            if len(tracks) == 0:
                self.respond(f"I'm sorry, I couldn't find any {genre} tracks on Spotify.")
            else:
                # Pick a random track from the search results
                random_track = random.choice(tracks)
                uri = random_track['uri']
                self.sp.start_playback(uris=[uri])
                self.respond(f"Now playing {random_track['name']} by {random_track['artists'][0]['name']}. Enjoy!")
        else:
            self.respond("I'm sorry, I couldn't authenticate with Spotify. Please try again later.")

This code uses the spotipy library to interact with the Spotify API. First, the YourAssistant class is initialized with the Spotify client ID and secret, and a token is obtained using the util.prompt_for_user_token method. The play_music method then searches for tracks of the specified genre using the sp.search method, and selects a random track from the search results. The URI of


    def get_news(self):

        # Set up API request
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.NEWS_API_KEY}"
        response = requests.get(url)
        articles = response.json()["articles"]

        # Iterate over articles and read titles to user
        for i, article in enumerate(articles):
            if i == 5:
                break # Limit to 5 articles
            title = article["title"]
            self.respond(f"Here's a headline: {title}")

    def open_browser(self, query):
        # Code to open browser and
        url = f"https://www.google.com/search?q={query}"
        webbrowser.get().open(url)
        self.respond(f"Here's what I found for {query}")
