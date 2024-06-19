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

time()