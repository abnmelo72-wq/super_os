# model_downloader.py

import os

def download_model(language_code):
    if language_code == 'ar':
        # نموذج عربي Vosk
        if not os.path.exists("models/vosk-ar"):
            os.system("mkdir -p models && cd models && wget https://alphacephei.com/vosk/models/vosk-model-small-ar-0.22.zip && unzip vosk-model-small-ar-0.22.zip && mv vosk-model-small-ar-0.22 vosk-ar && rm vosk-model-small-ar-0.22.zip")
        return "models/vosk-ar"
    elif language_code == 'en':
        # نموذج Whisper إنكليزي
        try:
            import whisper
            return "whisper:base"
        except ImportError:
            print("❌ مكتبة whisper غير مثبتة. ثبّتها بـ: pip install openai-whisper")
            return None
    else:
        print(f"⚠️ لا يوجد نموذج متاح للغة: {language_code}")
        return None
