import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyttsx3
import speech_recognition as sr

from actionList import assistantActions

listener = sr.Recognizer()

engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)



class assistant:

    def __init__(self, name, assistantActions:assistantActions):
        self.name = name 
        self.activate = True
        self.actionList = assistantActions


    def take_command(self):
        try:
            with sr.Microphone() as source:
                print('listening...')
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
                command = command.lower()
                print(command)
                if self.name in command:
                    command = command.replace(self.name, '')
            return command

        except:
            pass
    
    
    
    def Stop(self):
        self.activate = False

    def Start(self):
        while self.activate:
            command = self.take_command()
            if command is None:
                continue
            else:
                self.actionList.performAction(command)(command)


# elif 'play' in command:
#     song = command.replace('play', '')
#     self.talk('playing ' + song)
#     pywhatkit.playonyt(song)
# elif 'time' in command:
#     time = datetime.datetime.now().strftime('%I:%M %p')
#     self.talk('Current time is ' + time)
# elif 'tell me about' in command:
#     person = command.replace('tell me about', '')
#     info = wikipedia.summary(person, 1)
#     print(info)
#     self.talk(info)
# elif 'joke' in command:
#     self.talk(pyjokes.get_joke())
# elif 'turn off' in command:
#     self.Stop()
# else:
#     self.talk(text = 'Please say the command again.')