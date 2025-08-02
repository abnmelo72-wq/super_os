import sys
import os

# التأكد من أن المسار الرئيسي للمشروع في PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# استيراد الوحدة
from ai_core.commands.voice_to_text.voice_transcriber import voice_to_text

# المسار إلى الملف الصوتي (تأكد من وجوده مسبقاً بصيغة wav أو mp3)
audio_path = "../../../test_audio.wav"  # عدل حسب اسم الملف عندك
lang = "auto"  # أو "ar" للغة العربية

try:
    result = voice_to_text(audio_path, lang=lang)
    print("\nالنص المستخرج:\n", result)
except Exception as e:
    print(f"[❌] حدث خطأ: {e}")
