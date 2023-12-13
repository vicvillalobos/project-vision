from text_to_speech.tts import TextToSpeechManager
from speech_to_text.stt import SpeechToTextManager
from processing.gpt import GPTManager

stt = SpeechToTextManager()
tts = TextToSpeechManager()
gpt = GPTManager("Jarvis")


def callback(text):
    print("User said: " + text)
    gpt_response = gpt.ask(text)
    print("GPT said: " + gpt_response)
    tts.talk(gpt_response)


callback("We're starting our conversation now. Greetings!")

stt.start(callback)

callback("Hope to see you again, bye!")
