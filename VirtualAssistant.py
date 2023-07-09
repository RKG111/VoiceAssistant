import pyttsx3

import pyttsx3

from vosk import Model, KaldiRecognizer
from actionList import assistantActions
import pyaudio
import numpy as np
import json
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
model_path = r"D:\Python\jarvis\vosk-model-small-en-us-0.15"

model = Model(model_path)

class assistant:

    def __init__(self, name, assistantActions:assistantActions, voiceId=0):
        self.name = name 
        self.activate = True
        self.actionList = assistantActions
        self.engine = pyttsx3.init()       
        self.engine.setProperty('voice',self.engine.getProperty('voices')[voiceId].id)
        self.recognizer = KaldiRecognizer(model, 44100)
    
    def talk(self,text):
        self.engine.say(text)
        self.engine.runAndWait()

    def recognize_speech(self, audio_data):
        self.recognizer.AcceptWaveform(audio_data)
        result = self.recognizer.Result()
        # print(result)
        result = json.loads(result)
        # print(result)
        return result['text']
    
    def take_command(self):
        try:
            
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
            if self.name in recognized_text:
                # print(recognized_text)
                command = recognized_text.replace(self.name,'')
                return command
            return None
        except KeyboardInterrupt:
            print('Terminated')
            return 'turn off'
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
            elif 'turn off' in command :
                
                self.Stop()
            else:
                # print(command)
                self.actionList.performAction(command)(self,command)

