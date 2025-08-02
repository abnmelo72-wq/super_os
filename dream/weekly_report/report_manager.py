import os
import json
import datetime
from collections import Counter

# تحويل نص إلى كلام محلي
try:
    import pyttsx3
    tts_engine_local = pyttsx3.init()
except ImportError:
    tts_engine_local = None

# تحويل نص إلى كلام عبر الانترنت (جوجل)
try:
    from gtts import gTTS
except ImportError:
    gTTS = None

class ReportManager:
    def __init__(self, base_dir="dream/weekly_report"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _get_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def summarize_content(self, text, max_words=100):
        words = text.split()
        return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

    def analyze_statistics(self, text):
        words = text.lower().split()
        word_count = len(words)
        char_count = len(text)
        unique_words = len(set(words))
        common_words = Counter(words).most_common(5)
        return {
            "word_count": word_count,
            "char_count": char_count,
            "unique_words": unique_words,
            "common_words": common_words
        }

    def save_report(self, title, content, include_audio=True, audio_mode="local"):
        """
        حفظ التقرير:
        - title: عنوان التقرير
        - content: النص الكامل
        - include_audio: إذا بدك يحول الصوت
        - audio_mode: "local" لـ pyttsx3 أو "online" لـ gTTS
        """
        timestamp = self._get_timestamp()
        safe_title = title.replace(" ", "_").replace("/", "_")
        report_name = f"{timestamp}_{safe_title}"
        json_path = os.path.join(self.base_dir, f"{report_name}.json")

        summary = self.summarize_content(content)
        stats = self.analyze_statistics(content)

        report_data = {
            "title": title,
            "timestamp": timestamp,
            "summary": summary,
            "statistics": stats,
            "content": content
        }

        # حفظ ملف JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)

        print(f"✅ تم حفظ التقرير: {json_path}")

        # إنشاء ملف صوتي حسب الطريقة المطلوبة
        if include_audio:
            audio_path = os.path.join(self.base_dir, f"{report_name}.mp3")
            if audio_mode == "local":
                self._tts_local(f"ملخص التقرير: {summary}", audio_path)
            elif audio_mode == "online":
                self._tts_online(f"ملخص التقرير: {summary}", audio_path)
            else:
                print(f"⚠️ وضع الصوت '{audio_mode}' غير معروف.")
                return
            print(f"🎧 تم إنشاء الصوت: {audio_path}")

    def _tts_local(self, text, filepath):
        if tts_engine_local is None:
            print("⚠️ pyttsx3 غير متوفرة، لم يتم إنشاء الصوت المحلي.")
            return
        tts_engine_local.save_to_file(text, filepath)
        tts_engine_local.runAndWait()

    def _tts_online(self, text, filepath):
        if gTTS is None:
            print("⚠️ gTTS غير متوفرة، لم يتم إنشاء الصوت عبر الإنترنت.")
            return
        try:
            tts = gTTS(text, lang="ar")
            tts.save(filepath)
        except Exception as e:
            print(f"⚠️ خطأ أثناء إنشاء الصوت عبر الإنترنت: {e}")

    def list_reports(self):
        """يرجع قائمة أسماء ملفات التقارير JSON"""
        return sorted([f for f in os.listdir(self.base_dir) if f.endswith(".json")])

    def load_report(self, filename):
        """يحمل تقرير معين بالاسم"""
        path = os.path.join(self.base_dir, filename)
        if not os.path.exists(path):
            print(f"⚠️ التقرير {filename} غير موجود.")
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def print_report_summary(self, filename):
        report = self.load_report(filename)
        if not report:
            return
        print(f"--- تقرير: {report['title']} ---")
        print(f"التاريخ: {report['timestamp']}")
        print(f"الملخص: {report['summary']}")
        print("الإحصائيات:")
        for k, v in report['statistics'].items():
            print(f"  {k}: {v}")
        print("-" * 40)

# مثال استخدام مباشر
if __name__ == "__main__":
    manager = ReportManager()

    content = """
    اليوم قمنا بتطوير وحدة التقارير في النظام. 
    أضفنا التحليل الذكي، التلخيص، والصوتيات المرافقة.
    نعمل على ربط هذه الوحدة مع المساعد الذكي ObeyX ليكون أكثر فعالية.
    """

    manager.save_report("تقرير تطوير النظام", content, include_audio=True, audio_mode="local")

    print("\n📋 قائمة التقارير:")
    for rpt in manager.list_reports():
        manager.print_report_summary(rpt)
