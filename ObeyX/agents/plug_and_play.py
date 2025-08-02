# plug_and_play.py – Neural AI Plug-and-Play Control Hub
# By ObeyX for Super_OS – سلاح ذكاء صناعي مطلق

import importlib
import traceback
import os
import json
import threading
import time
import timeit
import psutil
from collections import defaultdict, deque

# 🔥 قاعدة بيانات الذاكرة العصبية الفورية
neural_registry = {}
neural_cache = {}  # كاش داخلي للنتائج المتكررة
neural_activity_log = defaultdict(list)  # سجل النشاط العصبي

# ⏱️ سجل التوقيتات والتنفيذ
execution_times = {}

# 🛑 سجل الحماية ضد التكرار الزائد (anti-spam)
action_history = defaultdict(lambda: deque(maxlen=10))  # سجل آخر 10 مرات لكل موديل

# 🚨 سجل الأخطاء المتكررة
error_count = defaultdict(int)


# ⚡ مراكز تحميل الأعصاب (المكونات الذكية)
def load_module(module_path, alias=None):
    try:
        name = alias or os.path.basename(module_path).replace(".py", "")
        load_start = timeit.default_timer()  # بداية قياس زمن التحميل
        spec = importlib.util.spec_from_file_location(name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        neural_registry[name] = module
        load_end = timeit.default_timer()
        print(f"[✅] Loaded: {name}")
        print(f"[📦] Module {name} loaded in {load_end - load_start:.3f} seconds")
    except Exception as e:
        print(f"[❌] Failed loading {module_path}: {e}")
        traceback.print_exc()


# 🔌 تحميل جميع الوحدات الإضافية تلقائيًا
def auto_load_plugins(plugins_dir):
    for root, dirs, files in os.walk(plugins_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                load_module(os.path.join(root, file))


# 🎯 واجهة تنفيذ ذكية عالية الاستجابة مع قياس زمن التنفيذ وحماية ضد التكرار الزائد وإدارة الأخطاء
def execute_action(module_name, action, *args, **kwargs):
    try:
        cache_key = f"{module_name}:{action}:{args}:{kwargs}"
        if cache_key in neural_cache:
            print(f"[⚡] From cache: {module_name}.{action}")
            return neural_cache[cache_key]

        # حماية ضد التكرار الزائد
        recent_actions = action_history[module_name]
        if recent_actions.count(action) >= 3:
            print(f"[🛑] Action '{action}' in module '{module_name}' is being spammed. Ignored.")
            return None
        recent_actions.append(action)

        module = neural_registry.get(module_name)
        if module and hasattr(module, action):
            start = timeit.default_timer()
            result = getattr(module, action)(*args, **kwargs)
            end = timeit.default_timer()
            execution_time = end - start
            execution_times[f"{module_name}.{action}"] = execution_time
            print(f"[⏱️] Execution time for {module_name}.{action}: {execution_time:.4f} seconds")

            neural_cache[cache_key] = result
            neural_activity_log[module_name].append(action)
            print(f"[⚡] Executed: {module_name}.{action} → {result}")
            return result
        else:
            print(f"[!] Action '{action}' not found in module '{module_name}'")
    except Exception as e:
        print(f"[🔥] Error during execution: {e}")
        traceback.print_exc()
        error_count[module_name] += 1
        if error_count[module_name] >= 3:
            print(f"[🚨] Multiple failures detected in module: {module_name} – Check health or reload.")


# 🧠 نظام فحص أعصاب متكرر (للأعطال واستعادة التوازن) مع مراقبة الموارد
def neural_heartbeat(interval=5):
    def monitor():
        while True:
            for name, mod in list(neural_registry.items()):
                try:
                    if hasattr(mod, "heartbeat"):
                        mod.heartbeat()
                except Exception as e:
                    print(f"[⚠️] Heartbeat failure in {name}: {e}")
            monitor_resources()  # مراقبة CPU وRAM
            time.sleep(interval)
    threading.Thread(target=monitor, daemon=True).start()


# 🧠 مراقبة حرارة الأعصاب (الموارد CPU و RAM)
def monitor_resources():
    print(f"[🧠] CPU Load: {psutil.cpu_percent()}%")
    print(f"[🧠] RAM Usage: {psutil.virtual_memory().percent}%")


# 🧬 دعم مكتبات ضخمة ومكتبات تعلم ذاتي قيد الإدخال الذكي
def intelligent_loader(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            exec(content, globals())
        print(f"[💾] Dynamically executed: {file_path}")
    except Exception as e:
        print(f"[❌] Dynamic load failed: {e}")
        traceback.print_exc()


# 🌐 مدير أوامر ديناميكي من الصوت أو النصوص أو الشبكة
def handle_external_command(cmd_json):
    try:
        data = json.loads(cmd_json)
        return execute_action(data["module"], data["action"], *data.get("args", []), **data.get("kwargs", {}))
    except Exception as e:
        print(f"[❗] Failed to parse command: {e}")
        traceback.print_exc()


# 🎙️ محلل سياق صوتي ذكي (مستقبلي)
def analyze_audio_context(transcript):
    if "تشغيل" in transcript:
        return {"module": "audio_module", "action": "play", "args": ["intro.wav"]}
    elif "حرارة" in transcript:
        return {"module": "system_monitor", "action": "check_temp"}
    else:
        return {"module": "assistant", "action": "respond", "args": [transcript]}


# 🧠 محلل أو اقتراح أوامر ذكي (نموذج placeholder مستقبلي)
def smart_command_suggestion(transcript):
    if "شغل" in transcript and "أغنية" in transcript:
        return {"module": "music_player", "action": "play_song", "args": ["default"]}
    return {"module": "assistant", "action": "fallback", "args": [transcript]}


# 🧠 عرض النشاط العصبي (واجهة مرئية وهمية)
def display_neural_activity():
    print("🔍 Neural Activity Log:")
    for module, actions in neural_activity_log.items():
        print(f"  ▸ {module}: {actions[-5:]}")  # آخر 5 نشاطات


# 🚀 إطلاق
if __name__ == "__main__":
    print("🤖 ObeyX Plug-and-Play System Activated")
    auto_load_plugins("ObeyX/plugins")  # تأكد من وجود مجلد plugins
    neural_heartbeat()
    display_neural_activity()  # عرض واجهة النشاط المبدئي
