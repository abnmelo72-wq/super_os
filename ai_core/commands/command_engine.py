from speech_to_text import auto_transcribe
from ai_core.commands.voice_to_text import transcribe_audio
import os
import sys
import time
import sounddevice as sd
import scipy.io.wavfile as wav

def run_command(command):
    if command == "سجل صوت":
        text = transcribe_audio()
        print("🧠 المساعد الذكي فهم:", text)
    else:
        print("⛔ أمر غير معروف:", command)

def print_with_typing(text, delay=0.02):
    """
    دالة لطباعة النص حرف حرف بشكل متدرج (تأثير كتابة)
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def process_text_command(command):
    """
    دالة لمعالجة أوامر نصية والرد عليها أو تنفيذ أوامر
    """
    command = command.lower().strip()

    if command in ["مرحبا", "اهلا", "السلام عليكم"]:
        print_with_typing("👋 مرحباً! كيف يمكنني مساعدتك؟")

    elif command in ["افتح الصوت", "شغل الصوت"]:
        print_with_typing("🔊 تم تشغيل الصوت.")  # مثال وهمي

    elif command in ["استمع", "تسجيل", "استمع لي"]:
        filename = record_voice()
        if filename:
            print_with_typing("📁 تم تسجيل الصوت. يتم تحويله الآن إلى نص...")
            text = auto_transcribe(filename)
            print_with_typing(f"📝 تم تحويل الصوت إلى نص: {text}")

    elif command in ["اطفئ الجهاز", "اغلق النظام"]:
        print_with_typing("⚠️ سيتم إيقاف تشغيل النظام...")
        time.sleep(2)
        os.system("shutdown now")

    else:
        print_with_typing("❓ لم أفهم الأمر: " + command)

def run_command_engine():
    """
    دالة لتشغيل المحرك النصي: استقبال أوامر المستخدم وتنفيذها
    """
    print_with_typing("📝 اكتب أمرك هنا (أو 'خروج' للخروج):")
    while True:
        try:
            user_input = input(">> ")
            if user_input.lower() in ["خروج", "exit", "quit"]:
                print_with_typing("👋 إلى اللقاء!")
                break
            process_text_command(user_input)
        except KeyboardInterrupt:
            print("\n👋 تم الإيقاف من قبل المستخدم.")
            break

def record_voice(filename="audio.wav", duration=4, fs=44100):
    """
    دالة لتسجيل الصوت لمدة معينة وحفظه في ملف WAV
    """
    print_with_typing("🎙️ تسجيل صوتي جاري... تحدث الآن!")
    try:
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        wav.write(filename, fs, audio)
        print_with_typing("✅ تم حفظ التسجيل الصوتي.")
        return filename
    except Exception as e:
        print_with_typing(f"❌ فشل تسجيل الصوت: {str(e)}")
        return None
