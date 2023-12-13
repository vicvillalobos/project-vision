import pyttsx3
from decouple import config


class TextToSpeechManager:
    def __init__(self):
        self.engine = pyttsx3.init("sapi5")
        self.engine.setProperty("rate", 200)
        self.engine.setProperty("volume", 1.0)
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[1].id)

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
