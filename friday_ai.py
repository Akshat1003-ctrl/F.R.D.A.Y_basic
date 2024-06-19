from gtts import gTTS
from playsound import playsound
import tempfile
import datetime
import speech_recognition as sr


def speak(audio):
    tts = gTTS(audio)
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name)
        playsound(fp.name)


def wishme():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Morning Mr. Chandra")
    elif 12 <= hour < 18:
        speak("Afternoon Mr. Chandra")
    elif 18 <= hour < 24:
        speak("Evening Mr. Chandra")
    else:
        speak("Hello Mr. Chandra")
    speak("FRIDAY at your service. Please tell me how I can assist you today")


def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak("The time currently is")
    speak(current_time)


def tell_date():
    current_date = datetime.datetime.now().strftime("%d %B %Y")
    speak("And the date currently is")
    speak(current_date)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("I didn't catch that. Could you say it again?")
        return None
    except sr.RequestError as e:
        speak(f"Could not request results from Google Speech Recognition service; {e}")
        return None


def handle_command(command):
    if 'time' in command:
        tell_time()
    elif 'date' in command:
        tell_date()
    elif 'who are you' in command or 'introduce yourself' in command:
        speak("I am FRIDAY, your personal assistant.")
    elif 'how are you' in command:
        speak("I am fine, thank you. How can I assist you today?")
    elif 'friday shutdown' in command:
        speak("Shutting down. Goodbye!")
        return False
    else:
        speak("I am not sure how to respond to that. Can you please repeat?")
    return True


wishme()
while True:
    command = take_command()
    if command:
        if not handle_command(command):
            break

