import os
import time
import sys

# فحص إذا داخل بيئة venv
if sys.prefix == sys.base_prefix:
    print("⚠️ يجب تشغيل السكربت داخل بيئة افتراضية venv.")
    sys.exit(1)

# اختيار الطريقة حسب سرعة الجهاز
USE_WHISPER = True  # غيّر لـ False إذا كان جهازك ضعيف

# تحديد ملف الإخراج
OUTPUT_TEXT_FILE = "spoken_text.txt"
AUDIO_FILE = "command.wav"

# تسجيل الصوت باستخدام ffmpeg
print("🎙️ تحدث الآن (5 ثواني)...")
os.system(f"ffmpeg -f alsa -i default -t 5 {AUDIO_FILE} -y > /dev/null 2>&1")
print("✅ تم التسجيل... جارٍ التحويل")

# تحليل الصوت
text_result = ""

if USE_WHISPER:
    import whisper
    model = whisper.load_model("base")  # اختر tiny أو base حسب قوة جهازك
    result = model.transcribe(AUDIO_FILE)
    text_result = result["text"]
else:
    import vosk
    import soundfile as sf
    from vosk import Model, KaldiRecognizer
    import wave
    import json

    # تأكد أن الموديل موجود
    if not os.path.exists("vosk-model-small-ar-0.22"):
        print("❌ موديل Vosk غير موجود! حمّله من: https://alphacephei.com/vosk/models")
        sys.exit(1)

    wf = wave.open(AUDIO_FILE, "rb")
    model = vosk.Model("vosk-model-small-ar-0.22")
    rec = KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            text_result += res.get("text", "") + " "

# حفظ الناتج في ملف
with open(OUTPUT_TEXT_FILE, "w", encoding="utf-8") as f:
    f.write(text_result.strip())

print("📄 الأمر الصوتي كنص:")
print("🧠", text_result.strip())
