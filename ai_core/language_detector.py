# language_detector.py

from langdetect import detect, DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException

# ضمان نتائج ثابتة
DetectorFactory.seed = 0

# قائمة اللغات المدعومة (اختياري للتحقق)
SUPPORTED_LANGUAGES = ['ar', 'en', 'de', 'fr', 'es', 'it', 'tr', 'ru']

def detect_language(text):
    """
    يكتشف اللغة الأكثر احتمالاً للنص المُعطى.

    :param text: نص المستخدم
    :return: رمز اللغة المكتشفة أو 'unknown'
    """
    try:
        # كشف أفضل لغة متوقعة
        language = detect(text)

        # التحقق من أن اللغة مدعومة
        if language in SUPPORTED_LANGUAGES:
            return language
        else:
            return 'unsupported'
    except LangDetectException:
        return 'unknown'
    except Exception as e:
        print(f"[language_detector] ⚠️ خطأ أثناء اكتشاف اللغة: {e}")
        return 'unknown'

def detect_language_probabilities(text):
    """
    يكتشف جميع اللغات المحتملة مع النسب المئوية (مفيد لتحليل أعمق أو تعليم ذاتي للمساعد).

    :param text: نص المستخدم
    :return: قائمة باللغات مع احتمالاتها أو [] في حال الخطأ
    """
    try:
        return detect_langs(text)
    except Exception as e:
        print(f"[language_detector] ⚠️ خطأ في كشف نسب اللغات: {e}")
        return []
