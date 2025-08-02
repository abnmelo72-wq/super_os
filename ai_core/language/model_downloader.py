# ai_core/language/model_downloader.py

import os
import shutil
import platform
import subprocess

def is_device_weak():
    try:
        cpu_info = subprocess.check_output("lscpu", shell=True).decode()
        if "ARM" in cpu_info or "Intel(R) Atom" in cpu_info or "Celeron" in cpu_info:
            return True
        if "MHz" in cpu_info:
            lines = cpu_info.splitlines()
            for line in lines:
                if "CPU MHz" in line:
                    mhz = float(line.split(":")[1].strip())
                    if mhz < 1800:
                        return True
    except:
        pass
    return False

def download_vosk_model(language_code):
    vosk_models = {
        'ar': 'https://alphacephei.com/vosk/models/vosk-model-ar-mgb2-0.4.zip',
        'en': 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip',
        'de': 'https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip',
        'fr': 'https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip',
        'es': 'https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip'
    }

    if language_code not in vosk_models:
        print(f"⚠️ لا يوجد نموذج Vosk للغة '{language_code}'")
        return None

    url = vosk_models[language_code]
    filename = url.split('/')[-1]
    model_name = filename.replace(".zip", "")
    model_path = f"models/{model_name}"

    if os.path.exists(model_path):
        print(f"✅ النموذج موجود بالفعل: {model_path}")
        return model_path

    os.makedirs("models", exist_ok=True)
    print(f"⬇️ يتم تنزيل نموذج Vosk للغة '{language_code}'...")
    os.system(f"wget -O models/{filename} {url}")
    os.system(f"unzip models/{filename} -d models/")
    print(f"📁 تم استخراج النموذج إلى: {model_path}")
    return model_path

def download_whisper_model(language_code):
    try:
        import whisper
    except ImportError:
        print("❌ مكتبة whisper غير مثبتة. ثبّتها باستخدام: pip install -U openai-whisper")
        return None

    # يمكن تغيير المستوى حسب مواصفات الجهاز
    if is_device_weak():
        model_name = "tiny"
    else:
        model_name = "base"

    print(f"🎙️ سيتم استخدام نموذج Whisper ({model_name}) للغة '{language_code}'")
    return f"whisper:{model_name}"

def download_model_for_language(language_code):
    weak_device = is_device_weak()

    if language_code in ['ar', 'en', 'de', 'fr', 'es']:
        if weak_device:
            return download_vosk_model(language_code)
        else:
            return download_whisper_model(language_code)
    else:
        print(f"⚠️ اللغة غير مدعومة مباشرة، سيتم محاولة استخدام Whisper")
        return download_whisper_model(language_code)
