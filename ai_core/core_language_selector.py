from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def get_lang_code(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"
