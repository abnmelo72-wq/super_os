from ai_core.speech_to_text.speech_engine import transcribe

def test_transcription():
    # مسار ملف صوتي محفوظ مسبقًا (WAV)
    audio_file = "audio.wav"
    
    # إذا اخترت Whisper
    text_whisper = transcribe(audio_file, lang="ar")
    print("نتيجة Whisper:")
    print(text_whisper)
    
    # إذا اخترت Vosk
    # عيّن USE_WHISPER = False داخل speech_engine.py لتجربة Vosk
    # وضع هنا مسار مجلد نموذج Vosk المناسب
    vosk_model_path = "path_to_vosk_model_ar"
    text_vosk = transcribe(audio_file, lang="ar", vosk_lang_path=vosk_model_path)
    print("نتيجة Vosk:")
    print(text_vosk)

if __name__ == "__main__":
    test_transcription()
