import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import platform

class VoiceAgent:
    def __init__(self, lang="en"):
        self.lang = lang
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
    
    def speech_to_text(self):
        with self.microphone as source:
            print("Listening... Please speak.")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio, language=self.lang)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google STT service; {e}")
            return None

    def text_to_speech(self, text):
        print(f"Speaking: {text}")
        tts = gTTS(text=text, lang=self.lang)
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
            tts.save(fp.name)
            # Cross-platform play sound
            if platform.system() == "Darwin":
                os.system(f"afplay {fp.name}")
            elif platform.system() == "Windows":
                os.system(f"start {fp.name}")
            else:  # Linux
                os.system(f"mpg123 {fp.name}")

# Quick local test
if __name__ == "__main__":
    va = VoiceAgent()
    text = va.speech_to_text()
    if text:
        va.text_to_speech(f"You said: {text}")
    else:
        va.text_to_speech("Sorry, I did not catch that.")
