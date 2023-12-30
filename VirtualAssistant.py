import pyttsx3

import pyttsx3

from vosk import Model, KaldiRecognizer
from actionList import assistantActions
import pyaudio
import numpy as np
import json
import time
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 70000 
DELAY_AFTER_SPEAKING = 1.0 
RECORD_SECONDS = 5.0
model_path = r"vosk-model-en-in-0.5"

model = Model(model_path)

class Assistant:

    def __init__(self, name, assistantActions:assistantActions, voiceId=0):
        self.name = name 
        self.activate = True
        self.actionList = assistantActions
        self.engine = pyttsx3.init()       
        self.engine.setProperty('voice',self.engine.getProperty('voices')[voiceId].id)
        self.recognizer = KaldiRecognizer(model, 44100)
        self.PortAudio = pyaudio.PyAudio()
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
        audio_frames = record_audio(self.PortAudio)
        # recognized_text=None
        command=None
        if audio_frames:
            audio_data = np.frombuffer(b''.join(audio_frames), dtype=np.int16).tobytes()
            recognized_text = self.recognize_speech(audio_data)
            print(recognized_text)
            if self.name in recognized_text:
                command=recognized_text.replace(self.name,'')
            
        return command       
        
        
    def Stop(self):
        self.activate = False

    def Start(self):
        try:
            while self.activate:
                command = self.take_command()
                # p = pyaudio.PyAudio()
                if command is None:
                    continue
                elif 'turn off' in command :
                
                    self.Stop()
                else:
                    # print(command)
                    self.actionList.performAction(command)(self,command)
        except KeyboardInterrupt:
            self.Stop()
            self.PortAudio.terminate()

def is_speaking(audio_data):
        volume_norm = np.linalg.norm(audio_data) * 10
        return volume_norm > THRESHOLD
    
def record_audio(p):
    frames = []
    speaking_start_time = 0
    recording_started = False
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    try:
        pre_buffer=[]
        while True:
            data = stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            if is_speaking(audio_data):
                if not recording_started:
                    recording_started = True
                    speaking_start_time = time.time()
                    frames.append(data)
                    continue
                else:
                    speaking_start_time = time.time()
                    # print("speaking"+ str(speaking_start_time))
                    frames.append(data)
            elif recording_started and time.time() - speaking_start_time < DELAY_AFTER_SPEAKING:
            
                frames.append(data)
            elif recording_started and time.time() - speaking_start_time > DELAY_AFTER_SPEAKING:
                frames.append(data)
                break
            
    finally:
        stream.stop_stream()
        stream.close()
    return frames