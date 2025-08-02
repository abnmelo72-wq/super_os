import os
import subprocess
import sys

# فحص إذا مكتبة whisper متاحة
USE_WHISPER = False
try:
    import whisper
    USE_WHISPER = True
except ImportError:
    USE_WHISPER = False

# فحص إذا مكتبة vosk متاحة
USE_VOSK = False
try:
    from vosk import Model, KaldiRecognizer
    import wave
    import json
    USE_VOSK = True
except ImportError:
    USE_VOSK = False


def recognize_with_whisper(audio_path):
    model = whisper.load_model("base")  # يمكن تغييره إلى "small" أو "medium"
    result = model.transcribe(audio_path)
    return result["text"]


def recognize_with_vosk(audio_path):
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        raise ValueError("Audio file must be WAV format mono PCM.")

    model_path = "model"  # يفترض أنك حملت نموذج VOSK المناسب هنا
    if not os.path.exists(model_path):
        raise FileNotFoundError("VOSK model folder not found")

    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            results.append(res.get("text", ""))
    final = json.loads(rec.FinalResult())
    results.append(final.get("text", ""))
    return " ".join(results)


def recognize(audio_path="input.wav"):
    if USE_WHISPER:
        print("🔊 باستخدام Whisper...")
        return recognize_with_whisper(audio_path)
    elif USE_VOSK:
        print("🔊 باستخدام Vosk...")
        return recognize_with_vosk(audio_path)
    else:
        raise RuntimeError("لم يتم العثور على مكتبة whisper أو vosk، يرجى تثبيتهما.")


if __name__ == "__main__":
    try:
        text = recognize()
        print("📄 النص المُستخرج:", text)
    except Exception as e:
        print("❌ حدث خطأ:", e)
