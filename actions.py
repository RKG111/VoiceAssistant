import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)



def talk(text):
    engine.say(text)
    engine.runAndWait()

def playYtMedia(command):
    song = command.replace('play', '')
    talk('playing ' + song)
    pywhatkit.playonyt(song)

def getCurrentTime(command):
    time = datetime.datetime.now().strftime('%I:%M %p')
    talk('Current time is ' + time)

def getInfo(command):
    person = command.replace('tell me about', '')
    info = wikipedia.summary(person, 1)
    # print(info)
    talk(info)

def joke(command):
    talk(pyjokes.get_joke())
