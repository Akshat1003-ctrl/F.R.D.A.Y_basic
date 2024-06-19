from __future__ import print_function
import datetime
import os.path
from gtts import gTTS
from playsound import playsound
import tempfile
import speech_recognition as sr
import requests
from googleapiclient.discovery import build

# API Key for Google Calendar
API_KEY = ''  # Replace with your Google API key
NEWS_API_KEY = ''  # Replace with your News API key


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


def fetch_news(query=None):
    if query:
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}'

    response = requests.get(url)
    news_data = response.json()

    if news_data['status'] == 'ok':
        if query:
            speak(f"Here are the top news articles about {query}.")
        else:
            speak("Here are the top news headlines for today.")
        for i, article in enumerate(news_data['articles'][:5], 1):
            speak(f"Headline {i}: {article['title']}")
            print(f"Headline {i}: {article['title']}")
    else:
        speak("I'm sorry, I couldn't fetch the news at the moment.")


def fetch_calendar_events(service, time_min, time_max, num_events=5):
    events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                          timeMax=time_max, maxResults=num_events, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events


def next_event(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events = fetch_calendar_events(service, now, '9999-12-31T23:59:59Z', 1)
    if not events:
        speak("You have no upcoming events.")
    else:
        event = events[0]
        start = event['start'].get('dateTime', event['start'].get('date'))
        speak(f"Your next event is {event['summary']} at {start}")


def today_events(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    end_of_day = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'
    events = fetch_calendar_events(service, now, end_of_day)
    if not events:
        speak("You have no events scheduled for today.")
    else:
        speak("Here are your events for today:")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            speak(f"Event: {event['summary']} at {start}")


def tomorrow_events(service):
    start_of_day = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'
    end_of_day = (datetime.datetime.utcnow() + datetime.timedelta(days=2)).isoformat() + 'Z'
    events = fetch_calendar_events(service, start_of_day, end_of_day)
    if not events:
        speak("You have no events scheduled for tomorrow.")
    else:
        speak("Here are your events for tomorrow:")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            speak(f"Event: {event['summary']} at {start}")


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


def handle_command(command, service):
    if 'time' in command:
        tell_time()
    elif 'date' in command:
        tell_date()
    elif 'news' in command:
        if 'about' in command:
            query = command.split('about')[1].strip()
            fetch_news(query)
        else:
            fetch_news()
    elif 'calendar' in command or 'events' in command:
        if 'next event' in command:
            next_event(service)
        elif 'today' in command:
            today_events(service)
        elif 'tomorrow' in command:
            tomorrow_events(service)
        else:
            speak("I can help you with information about your calendar. You can ask about your next event, events for today, or events for tomorrow.")
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


def main():
    service = build('calendar', 'v3', developerKey=API_KEY)
    wishme()
    while True:
        command = take_command()
        if command:
            if not handle_command(command, service):
                break


if __name__ == '__main__':
    main()
