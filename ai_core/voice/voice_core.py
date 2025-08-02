# voice_core.py
from listen import record_voice
from speech_to_text import transcribe_audio
from language_detector import detect_language

def run_voice():
    path = record_voice()
    text = transcribe_audio(path)
    lang = detect_language(text)
    print(f"📝 النص: {text}")
    print(f"🌍 اللغة: {lang}")
    return text, lang
