import os
import sys
import wave
import contextlib
import subprocess
from faster_whisper import WhisperModel

def transcribe(audio_path: str, model_size: str = "small", language: str = "ar") -> str:
    # تأكد من أن الملف موجود
    if not os.path.exists(audio_path):
        print(f"❌ الملف {audio_path} غير موجود.")
        return ""

    # تحقق من طول الملف الصوتي
    with contextlib.closing(wave.open(audio_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        if duration > 60:
            print("⚠️ التحذير: الملف أطول من دقيقة. سيتم اقتصاصه لأول 60 ثانية.")
            audio_path_cut = "/tmp/cut_audio.wav"
            subprocess.run(["ffmpeg", "-i", audio_path, "-t", "60", audio_path_cut, "-y"])
            audio_path = audio_path_cut

    # تحميل النموذج
    model = WhisperModel(model_size, compute_type="int8")

    # تحويل الصوت إلى نص
    segments, _ = model.transcribe(audio_path, language=language)

    # جمع النتائج
    result = ""
    for segment in segments:
        result += segment.text + " "
    return result.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ الاستعمال: python transcriber.py path_to_audio.wav")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    print("🔍 جاري تحويل الصوت إلى نص...")
    text = transcribe(audio_file)
    print("\n📄 النص الناتج:")
    print(text)
