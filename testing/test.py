import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from vosk import Model, KaldiRecognizer
import pyaudio
import numpy as np

model_path = r"D:\Python\jarvis\vosk-model-small-en-us-0.15"

model = Model(model_path)
recognizer = KaldiRecognizer(model, 44100)

engine = pyttsx3.init()

class Assistant:
    def __init__(self, name):
        self.name = name
        self.activate = True

    def talk(self, text):
        engine.say(text)
        engine.runAndWait()

    def playYtMedia(self, command):
        song = command.replace('play', '')
        self.talk('playing ' + song)
        pywhatkit.playonyt(song)

    def getCurrentTime(self, command):
        time = datetime.datetime.now().strftime('%I:%M %p')
        self.talk('Current time is ' + time)

    def getInfo(self, command):
        person = command.replace('tell me about', '')
        info = wikipedia.summary(person, 1)
        self.talk(info)

    def joke(self, command):
        self.talk(pyjokes.get_joke())

    def recognize_speech(self, audio_data):
        recognizer.AcceptWaveform(audio_data)
        result = recognizer.Result()
        print(result)
        return result[14:-3]

    def take_command(self):
        try:
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            RECORD_SECONDS = 5

            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            frames = []
            for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16).tobytes()

            recognized_text = self.recognize_speech(audio_data)
            return recognized_text

        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def Stop(self):
        self.activate = False

    def Start(self):
        while self.activate:
            command = self.take_command()
            if command is None:
                continue
            elif 'play' in command:
                song = command.replace('play', '')
                self.talk('playing ' + song)
                pywhatkit.playonyt(song)
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                self.talk('Current time is ' + time)
            elif 'tell me about' in command:
                person = command.replace('tell me about', '')
                info = wikipedia.summary(person, 1)
                print(info)
                self.talk(info)
            elif 'joke' in command:
                self.talk(pyjokes.get_joke())
            elif 'turn off' in command:
                self.Stop()
            else:
                self.talk('Please say the command again.')


# Example usage
assistant = Assistant("Nova")
assistant.Start()
