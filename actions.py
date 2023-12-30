import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyttsx3
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)



# def talk(text):
#     engine.say(text)
#     engine.runAndWait()

def playYtMedia(ai,command):
    try:
    # print('called')
        song = command.replace('play', '')
        ai.talk('playing ' + song)
        pywhatkit.playonyt(song)
    except:
        ai.talk('Please connect to a network')

def getCurrentTime(ai,command):
    try:
        time = datetime.datetime.now().strftime('%I:%M %p')
        ai.talk('Current time is ' + time)
    except:
        ai.talk('Please connect to a network')
def getInfo(ai,command):
    try:
        person = command.replace('tell me about', '')
        info = wikipedia.summary(person, 1)
        # print(info)
        ai.talk(info)
    except:
        ai.talk('Please connect to a network')
def joke(ai,command):
    try:
        ai.talk(pyjokes.get_joke())
    except:
        ai.talk('Please connect to a network')