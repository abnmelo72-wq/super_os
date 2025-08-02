import os
import whisper
import wave
import json
import torch
from vosk import Model, KaldiRecognizer

def get_cpu_load():
    try:
        with open("/proc/loadavg", "r") as f:
            load = float(f.read().split()[0])
        return load
    except:
        return 0.0

def transcribe_with_whisper(filename):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(filename)
        return result["text"]
    except Exception as e:
        return f"[Whisper Error]: {str(e)}"

def transcribe_with_vosk(filename):
    try:
        wf = wave.open(filename, "rb")
        if wf.getnchannels() != 1:
            return "[Vosk Error] Only mono audio supported"
        model = Model(lang="ar")
        rec = KaldiRecognizer(model, wf.getframerate())
        result = ""

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                result += part_result.get("text", "") + " "

        final_result = json.loads(rec.FinalResult())
        result += final_result.get("text", "")
        return result.strip()
    except Exception as e:
        return f"[Vosk Error]: {str(e)}"

def auto_transcribe(filename):
    load = get_cpu_load()
    if load < 1.5 and torch.cuda.is_available():
        return transcribe_with_whisper(filename)
    else:
        return transcribe_with_vosk(filename)
