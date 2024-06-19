from gtts import gTTS
from playsound import playsound
import tempfile
import datetime



def speak(audio):
    tts = gTTS(audio)
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name)
        playsound(fp.name)


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(Time)

def date()
    Date = datetime.datetime.now().strftime("%d %B %Y")
     speak(Date)

speak("The time currently is")
time()
speak("And the date currently is")
date()
