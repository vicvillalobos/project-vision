import speech_recognition as sr


class SpeechToTextManager:
    def __init__(self) -> None:
        self.run = False

    def start(self, callback=None):
        self.run = True
        self.listen_loop(callback)

    def stop(self):
        self.run = False

    def listen_loop(self, callback=None):
        while self.run:
            text = self.listen()
            if text == "stop":
                self.run = False
                return
            if callback:
                callback(text)

    def listen(self):
        with sr.Microphone() as source:
            try:
                r = sr.Recognizer()
                print("Say something!")
                audio = r.listen(source)
                text = r.recognize_google(audio)
            except:
                text = "error"
        return text
