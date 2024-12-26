import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import pyjokes
import datetime


import pywhatkit as kit
import pyautogui
import requests
from bs4 import BeautifulSoup



# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    """Listen to the user's voice command and return it as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return "None"
    return query.lower()


def tell_joke():
    """Tell a random joke."""
    joke = pyjokes.get_joke()
    return joke


def get_greeting():
    """Return a greeting based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"


def get_time_and_date():
    """Return the current time and date."""
    now = datetime.datetime.now()
    date = now.strftime("%B %d, %Y")
    time = now.strftime("%I:%M %p")
    return f"Today is {date}, and the current time is {time}."



def search_google(query):
    """Perform a Google search."""
    kit.search(query)


import os

import os


def take_screenshot():
    """Take a screenshot using PyAutoGUI and save it to D:/ss folder with unique filenames."""
    # Check if the folder exists, and if not, create it
    if not os.path.exists("D:/ss"):
        os.makedirs("D:/ss")

    # Get the number of existing files in the folder to generate a unique filename
    existing_files = os.listdir("D:/ss")
    screenshot_count = len([file for file in existing_files if file.startswith("screenshot") and file.endswith(".png")])

    # Generate the filename
    filename = f"D:/ss/screenshot{screenshot_count + 1}.png"

    # Take the screenshot and save it with the new filename
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    speak(f"Screenshot taken and saved as {filename}.")



def web_scrape():
    """Perform a web scrape to get a live webpage."""
    url = 'https://example.com'  # Replace with any URL you want to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.title)
    return soup.title.string


if __name__ == '__main__':
    greeting = get_greeting()
    speak(f"{greeting} Hello kayes How can I assist you today?")

    while True:
        query = takeCommand()

        if 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif 'open' in query:
            # Extract the name of the website and open it
            site = query.replace('open', '').strip()
            speak(f"Opening {site}")
            webbrowser.open(f"https://{site}.com")
        elif 'who is' in query or 'what is' in query:
            try:
                speak("Let me search that for you.")
                result = wikipedia.summary(query, sentences=2)
                print(result)
                speak(result)
            except Exception as e:
                speak("Sorry, I couldn't find any information on that.")
        elif 'search' in query:
            search_term = query.replace('search', '').strip()
            if search_term:
                speak(f"Searching for {search_term} on Google")
                search_google(search_term)
            else:
                speak("Please specify what you'd like me to search for.")
        elif 'joke' in query:
            joke = tell_joke()
            speak(joke)
            print(joke)
        elif 'date' in query or 'time' in query:
            time_date = get_time_and_date()
            speak(time_date)
            print(time_date)



        elif 'screenshot' in query:
            take_screenshot()


        elif 'scrape' in query:
            title = web_scrape()
            speak(f"The title of the webpage is: {title}")
        elif 'bye' in query or 'exit' in query:
            speak("Goodbye! Have a nice day!")
            break
        else:
            print("Sorry, I can only perform certain actions. Please try again.")
