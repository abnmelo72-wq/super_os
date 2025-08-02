import os
import sys
import json
import shutil
import sounddevice as sd
import queue
import tempfile
import numpy as np
import threading

from vosk import Model as VoskModel, KaldiRecognizer
import whisper

USE_WHISPER = False  # سيتم ضبطه تلقائيًا حسب الأداء

q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Error: {status}", file=sys.stderr)
    q.put(bytes(indata))

def record_audio(seconds=5, samplerate=16000):
    print("🎙️ تسجيل صوت لمدة", seconds, "ثواني...")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        with open(filename, 'wb') as wf:
            for _ in range(0, int(samplerate / 8000 * seconds)):
                wf.write(q.get())
    print("✅ تم التسجيل:", filename)
    return filename

def transcribe_with_vosk(audio_file):
    model_path = "ai_core/models/vosk"
    if not os.path.isdir(model_path):
        print("⏬ تحميل نموذج Vosk...")
        os.makedirs(model_path, exist_ok=True)
        # حمّل النموذج المناسب يدوياً أو ضع رابط التنزيل التلقائي إن أردت
        print("⚠️ حمّل النموذج يدويًا وضعه في:", model_path)
        return ""

    model = VoskModel(model_path)
    rec = KaldiRecognizer(model, 16000)
    with open(audio_file, "rb") as f:
        data = f.read()
        if rec.AcceptWaveform(data):
            result = rec.Result()
        else:
            result = rec.FinalResult()
    text = json.loads(result).get("text", "")
    print("🗣️ نص مستخرج (Vosk):", text)
    return text

def transcribe_with_whisper(audio_file):
    print("📥 جاري التحويل باستخدام Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    print("🗣️ نص مستخرج (Whisper):", result["text"])
    return result["text"]

def transcribe_audio(auto_select=True):
    audio = record_audio()

    if auto_select:
        ram = shutil.disk_usage("/")[2] // (1024 * 1024)
        USE_WHISPER = ram > 2048  # أكثر من 2GB؟ استخدم Whisper
    try:
        return transcribe_with_whisper(audio) if USE_WHISPER else transcribe_with_vosk(audio)
    finally:
        os.remove(audio)
