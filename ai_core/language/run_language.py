# run_language.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# تأكد من إضافة المسار الصحيح للوحدات
sys.path.append("ai_core/language")

from core_language_selector import detect_language
from model_downloader import download_model_for_language

if __name__ == "__main__":
    print("🎙️ بدء الكشف عن اللغة...")

    # إدخال من المستخدم
    text = input("📝 الرجاء إدخال جملة للكشف عن اللغة: ").strip()

    if not text:
        print("⚠️ لم يتم إدخال أي نص. يرجى المحاولة مرة أخرى.")
        sys.exit(1)

    # محاولة كشف اللغة
    lang = detect_language(text)

    if lang:
        print(f"✅ تم اكتشاف اللغة: {lang}")
        print("⬇️ جاري تنزيل النموذج المناسب...")
        download_model_for_language(lang)
    else:
        print("❌ لم يتم الكشف عن اللغة. حاول مجددًا.")
