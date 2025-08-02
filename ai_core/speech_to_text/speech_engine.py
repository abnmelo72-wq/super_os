import whisper
import os

def transcribe(audio_path, lang="ar"):
    """
    تحويل ملف صوتي إلى نص باستخدام Whisper
    """
    try:
        model_name = "medium" if lang in ["ar", "de", "ru"] else "base"
        print(f"[+] تحميل النموذج: {model_name}")
        model = whisper.load_model(model_name)

        print(f"[🎧] تحليل الملف الصوتي: {audio_path}")
        result = model.transcribe(audio_path, language=lang)

        print(f"[📝] النص المستخرج: {result['text']}")
        return result["text"]
    except Exception as e:
        print(f"[❌] خطأ في تحويل الصوت: {str(e)}")
        return ""
