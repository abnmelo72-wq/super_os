import os
import requests
import zipfile

# خريطة اللغة → رابط النموذج
VOSK_MODELS = {
    "ar": "https://alphacephei.com/vosk/models/vosk-model-small-ar-0.22.zip",
    "en": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
    "de": "https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip"
}

def download_and_extract(language_code):
    if language_code not in VOSK_MODELS:
        print(f"❌ اللغة {language_code} غير مدعومة حالياً.")
        return

    url = VOSK_MODELS[language_code]
    model_name = url.split("/")[-1]
    save_path = f"models/{model_name}"
    extract_dir = f"models/{model_name.replace('.zip', '')}"

    if os.path.exists(extract_dir):
        print(f"✅ النموذج '{language_code}' مثبت مسبقًا.")
        return

    print(f"⬇️ تحميل النموذج: {url}")
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"📦 فك الضغط...")
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall("models")

    os.remove(save_path)
    print(f"✅ تم التثبيت في: {extract_dir}")

# مثال: لاحقًا استبدل 'ar' باكتشاف اللغة تلقائيًا
download_and_extract("ar")
