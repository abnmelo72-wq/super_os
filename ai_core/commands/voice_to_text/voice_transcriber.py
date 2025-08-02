import os
from ai_core.speech_to_text.speech_engine import transcribe

def voice_to_text(audio_path, lang="auto"):
    """
    يستخدم Whisper أو Vosk لتحويل ملف صوتي إلى نص.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"الملف غير موجود: {audio_path}")
    
    print(f"[🔊] جاري تحويل الملف الصوتي إلى نص: {audio_path}")
    text = transcribe(audio_path, lang=lang)
    
    print(f"[✅] النص المستخرج: {text}")
    return text
