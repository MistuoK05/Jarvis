import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from gtts import gTTS
import pygame

load_dotenv()
recognizer = sr.Recognizer()
engine=pyttsx3.init()
apiKey = os.getenv("NEWS_API_KEY")
# client=OpenAI(api_key = os.getenv("OPENAI_API_KEY"))


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def aiProcess(command):
    completion = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a short-response virtual assistant named Jarvis."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

# def aiProcess(command):
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud,give short responeces"},
#             {"role": "user", "content": command}
#         ]
#     )
#     return completion.choices[0].message.content
    
def speak_OLD(text):
    engine = pyttsx3.init(driverName='sapi5')
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('text.mp3')
    # Initialize pygame mixer

    pygame.mixer.init()

    # Load your MP3 file
    pygame.mixer.music.load('text.mp3')
    # Play the music (loops=0 means play once, -1 means loop forever)
    pygame.mixer.music.play()

    # Keep the program running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) 

    pygame.mixer.music.unload()
    os.remove('text.mp3')  # Clean up the temporary file    


def processCommand(c):
    if("open google" in c.lower()):
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif("open youtube" in c.lower()):
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif("open facebook" in c.lower()):    
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif("open twitter" in c.lower()):
        speak("Opening Twitter")
        webbrowser.open("https://www.twitter.com")
    elif("open instagram" in c.lower()):
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif("open whatsapp" in c.lower()):
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")                
    elif("open linkein" in c.lower()):
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musiclibrary.music[song]
        webbrowser.open(link)

    elif c.lower().startswith("search"):
        query=c.lower().split(" ")[1]
        speak("Searching for " + query)
        webbrowser.open("https://www.google.com/search?q=" + query)    
    
    elif "news" in c.lower():
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={apiKey}"
        speak("Fetching the latest news")
    
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            articles = data.get("articles", [])
            
            for article in articles:
                speak(article["title"])
                
        else:
            speak(f"Error fetching news, status code {response.status_code}")
    
    else:
        output = aiProcess(c)
        speak(output)

if __name__=="__main__":
    speak("Initializing Jarvis......")
    while True:
        print("recognizing...")
        
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source,timeout=10,phrase_time_limit=5)

            WIEK_WORD= recognizer.recognize_google(audio)    
            if (WIEK_WORD.lower() == "jarvis"):
                speak("Ya")
                with sr.Microphone() as source:
                    print("jarvis Active...")
                    audio = recognizer.listen(source)
                command= recognizer.recognize_google(audio)
                
                processCommand(command)

        except Exception as e:
            print("error; {0}".format(e))       

