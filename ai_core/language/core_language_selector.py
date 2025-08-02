# core_language_selector.py

from ai_core.language_detector import detect_language

# يحدد النموذج الصوتي المناسب حسب اللغة المكتشفة
def select_model_by_language(text):
    lang = detect_language(text)

    # ملاحظة: بإمكانك لاحقاً ربط كل لغة بموديل whisper أو vosk حسب الموارد
    if lang == 'ar':
        return 'arabic-model'  # placeholder
    elif lang == 'en':
        return 'english-model'
    elif lang == 'de':
        return 'german-model'
    else:
        return 'default-model'
