import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)  # سرعة الكلام
    engine.setProperty('volume', 1.0)  # مستوى الصوت

    engine.say(text)
    engine.runAndWait()
