import time
import traceback
import random
import importlib

from speech_to_text.whisper_engine import transcribe_whisper
from speech_to_text.vosk_engine import transcribe_vosk
from language.text_llm import generate_response

# قاعدات بيانات صغيرة مدمجة
performance_log = {}
error_memory = []
task_history = []
model_scores = {
    "whisper": [],
    "vosk": [],
    "llm": [],
}
dynamic_model_registry = {}

# 📊 سجل الأداء والذكاء
def log_performance(task_name, start_time, model_name=None):
    elapsed = round(time.time() - start_time, 3)
    performance_log[task_name] = f"{elapsed}s"
    if model_name:
        model_scores.setdefault(model_name, []).append(elapsed)
    print(f"[ModelDispatcher] ✅ Task: {task_name} | Time: {elapsed}s | Model: {model_name}")

# 🧠 سجل أخطاء ذكي
def log_error(task_type, error):
    error_info = {
        "task": task_type,
        "error": str(error),
        "trace": traceback.format_exc()
    }
    error_memory.append(error_info)
    print(f"[ModelDispatcher] ⚠️ Error captured in task '{task_type}': {error}")

# 🔍 تحليل أداء النماذج الذكي
def get_best_model(models):
    best_model = None
    best_avg = float("inf")
    for model in models:
        times = model_scores.get(model, [])
        if times:
            avg = sum(times) / len(times)
            if avg < best_avg:
                best_model = model
                best_avg = avg
    return best_model or random.choice(models)

# 🧠 اختيار النموذج بناء على اللغة والذكاء الذاتي
def smart_model_selection(task_type, lang, options):
    if task_type == "speech_to_text":
        if lang == "ar":
            return get_best_model(["whisper"])
        elif lang in ["en", "de", "fr"]:
            return get_best_model(["vosk", "whisper"])
        else:
            return random.choice(["whisper", "vosk"])
    elif task_type == "text_generation":
        return "llm"
    return "default"

# 📦 تحميل ديناميكي لأي نموذج مستقبلي
def dynamic_import(module_path, function_name):
    module = importlib.import_module(module_path)
    return getattr(module, function_name)

# 🧠 الوحدة المركزية فائقة الذكاء لتوزيع المهام
def dispatch_model(task_type, data, lang="auto", options=None):
    if options is None:
        options = {}

    try:
        start = time.time()
        task_history.append(task_type)

        selected_model = smart_model_selection(task_type, lang, options)

        if task_type == "speech_to_text":
            engine = options.get("engine", selected_model)

            try:
                if engine == "whisper":
                    result = transcribe_whisper(data, lang=lang)
                elif engine == "vosk":
                    result = transcribe_vosk(data, lang=lang)
                else:
                    raise ValueError("Unknown STT engine.")

            except Exception:
                print(f"[ModelDispatcher] ⚠️ '{engine}' failed. Trying fallback...")
                fallback = "vosk" if engine == "whisper" else "whisper"
                result = dispatch_model("speech_to_text", data, lang, {"engine": fallback})

            log_performance("speech_to_text", start, engine)
            return result

        elif task_type == "text_generation":
            result = generate_response(data, context=options.get("context", ""))
            log_performance("text_generation", start, "llm")
            return result

        elif task_type == "translation":
            translator = dynamic_import("language.translator", "translate_text")
            result = translator(data, target_lang=lang)
            log_performance("translation", start, "translator")
            return result

        elif task_type == "image_analysis":
            analyzer = dynamic_import("vision.vision_engine", "analyze_image")
            result = analyzer(data)
            log_performance("image_analysis", start, "vision_engine")
            return result

        elif task_type in dynamic_model_registry:
            model_func = dynamic_model_registry[task_type]
            result = model_func(data)
            log_performance(task_type, start, model_func.__name__)
            return result

        else:
            raise ValueError(f"❌ Unknown task type: {task_type}")

    except Exception as e:
        log_error(task_type, e)
        return {
            "status": "error",
            "message": "🚨 حدث خطأ أثناء تنفيذ المهمة.",
            "details": str(e)
        }

# 📈 وحدة تشخيص ذكية
def diagnostics():
    return {
        "performance_log": performance_log,
        "recent_errors": error_memory[-5:],
        "task_history": task_history[-20:],
        "model_averages": {
            model: round(sum(times) / len(times), 3) if times else None
            for model, times in model_scores.items()
        }
    }

# 🧠 تعلم ذاتي مستقبلي
def learn_from_usage():
    print("[ModelDispatcher] 🧠 Self-learning activated (v2+). Future integration: DB & Reinforcement Learning")

# 🔌 تسجيل موديلات مخصصة خارجية
def register_custom_model(task_type, function):
    dynamic_model_registry[task_type] = function
    print(f"[ModelDispatcher] 📥 Registered external model for '{task_type}'.")
