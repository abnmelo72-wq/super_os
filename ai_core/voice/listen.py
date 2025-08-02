# listen.py
import sounddevice as sd
import numpy as np
import wave
import os
from datetime import datetime

def record_voice(duration=5, fs=16000):
    print("🎤 تسجيل جاري... (5 ثواني)")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    
    filename = f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    path = os.path.join("recordings", filename)
    os.makedirs("recordings", exist_ok=True)

    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())

    print(f"💾 تم حفظ التسجيل في: {path}")
    return path
