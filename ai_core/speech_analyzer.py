# speech_analyzer.py
import os
from ai_core.language.core_language_selector import get_model_for_language
from ai_core.voice.model_downloader import download_model

def prepare_speech_model_for_text(text):
    lang = get_model_for_language(text)
    model_name = download_model(lang)
    return model_name
