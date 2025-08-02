# speech_to_text.py
import os
import platform
import psutil
import whisper
import vosk
import wave
import json

def get_system_capability():
    try:
        ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        cpu_count = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq().max if psutil.cpu_freq() else 0

        if ram_gb >= 4 and cpu_count >= 4 and cpu_freq >= 2000:
            return "high"
        else:
            return "low"
    except:
        return "low"

def transcribe_with_whisper(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def transcribe_with_vosk(audio_path):
    model_path = "models/vosk-model-small-ar"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"نموذج Vosk غير موجود في {model_path}")

    model = vosk.Model(model_path)
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
        raise ValueError("يجب أن يكون الصوت بتنسيق 16kHz WAV mono")

    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    results = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results += part_result.get("text", "") + " "

    final_result = json.loads(rec.FinalResult())
    results += final_result.get("text", "")
    return results.strip()

def transcribe_audio(audio_path):
    capability = get_system_capability()

    if capability == "high":
        print("🎙️ يستخدم Whisper (جهاز قوي)")
        return transcribe_with_whisper(audio_path)
    else:
        print("🎙️ يستخدم Vosk (جهاز متوسط/ضعيف)")
        return transcribe_with_vosk(audio_path)
