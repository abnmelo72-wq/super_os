import os
import sys
import argparse

# المسارات النسبية
sys.path.append(os.path.expanduser("~/super_os/ai_core/audio"))
sys.path.append(os.path.expanduser("~/super_os/ai_core/utils/text_cleaner"))

from download_model import get_model
from auto_model_downloader import recognize_speech_auto
from cleaner import clean_text

def main():
    parser = argparse.ArgumentParser(description="تحويل الصوت إلى نص مع تنظيفه")
    parser.add_argument("audio_file", help="ملف صوتي بصيغة WAV")

    args = parser.parse_args()
    audio_path = args.audio_file

    # التحقق من وجود الملف
    if not os.path.exists(audio_path):
        print(f"[❌] الملف غير موجود: {audio_path}")
        return

    # تحميل الموديل المناسب حسب اللغة
    get_model(audio_path)

    # تنفيذ التعرف على الصوت
    raw_text = recognize_speech_auto(audio_path)

    print(f"\n🔤 النص الأصلي:\n{raw_text}")

    # تنظيف النص
    cleaned_text = clean_text(raw_text)
    print(f"\n🧼 النص بعد التنظيف:\n{cleaned_text}")

if __name__ == "__main__":
    main()
