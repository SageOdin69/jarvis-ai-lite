"""import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

def speak(text):
    print("\nJarvis:", text)
    print("DEBUG: Speaking now...")   # ← add this
    engine.say(text)
    engine.runAndWait()"""
    
import pyttsx3

def speak(text):
    print("\nJarvis:", text)

    engine = pyttsx3.init('sapi5')  # create fresh engine each time
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()