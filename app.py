from flask import Flask, jsonify, request
import pyttsx3
import wikipedia
import pyjokes
import datetime
import pywhatkit as kit
import pyautogui
import requests
from bs4 import BeautifulSoup

# Initialize the Flask app
app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

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

@app.route('/assistant', methods=['POST'])
def assistant():
    query = request.json.get('query', '').lower()

    if 'joke' in query:
        joke = tell_joke()
        speak(joke)
        return jsonify({"response": joke})
    elif 'date' in query or 'time' in query:
        time_date = get_time_and_date()
        speak(time_date)
        return jsonify({"response": time_date})
    elif 'search' in query:
        search_term = query.replace('search', '').strip()
        if search_term:
            speak(f"Searching for {search_term} on Google")
            kit.search(search_term)
            return jsonify({"response": f"Searching for {search_term} on Google"})
        else:
            return jsonify({"response": "Please specify what you'd like me to search for."})
    elif 'who is' in query or 'what is' in query:
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result)
            return jsonify({"response": result})
        except Exception as e:
            return jsonify({"response": "Sorry, I couldn't find any information on that."})
    elif 'bye' in query or 'exit' in query:
        speak("Goodbye! Have a nice day!")
        return jsonify({"response": "Goodbye! Have a nice day!"})
    else:
        return jsonify({"response": "Sorry, I can only perform certain actions. Please try again."})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
