# context_engine.py
"""
وحدة تحليل السياق الذكي - Context Engine
لـ ObeyX في نظام Super_OS
"""

import os
import json
import threading
import traceback
import time
import queue
from collections import defaultdict, deque
from datetime import datetime

# مكتبات علمية وتقنية لدعم الذكاء الاصطناعي (ممكن إضافتها لاحقًا)
try:
    import numpy as np
    import pandas as pd
except ImportError:
    # إذا غير مثبتة، نرسل تحذير فقط ولا نوقف العمل
    print("[⚠️] Warning: numpy/pandas not found. Some advanced features disabled.")

# ----------------------------------------
# إعدادات أساسية
MAX_QUEUE_SIZE = 1000  # الحد الأقصى لعمليات التحليل المعلقة
CACHE_EXPIRY_SECONDS = 600  # وقت صلاحية الكاش 10 دقائق

# ----------------------------------------
# الذاكرة المؤقتة وذاكرة السياق
context_cache = {}
context_cache_timestamps = {}

# سجل الأحداث والعمليات (مع تخزين محدد)
event_log = deque(maxlen=5000)

# قائمة انتظار للأوامر أو البيانات المراد تحليلها
input_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# ----------------------------------------
# سجل الأخطاء المتكرر لمنع التوقف التام
error_counter = defaultdict(int)

# ----------------------------------------
# الوظائف الأساسية للوحدة

def safe_execute(func):
    """
    Decorator لضمان عدم توقف وحدة السياق بسبب خطأ في تحليل معين
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_counter[func.__name__] += 1
            print(f"[❗] Error in {func.__name__}: {e}")
            traceback.print_exc()
            # عند حدوث أكثر من 5 أخطاء متتالية نرسل إنذار للنظام الأعلى
            if error_counter[func.__name__] >= 5:
                notify_obeyx_critical(f"Repeated errors in {func.__name__}")
                error_counter[func.__name__] = 0
            return None
    return wrapper

def notify_obeyx_critical(message):
    """
    إرسال تنبيه لـ ObeyX بخصوص أخطاء حرجة
    """
    print(f"[🚨] Critical Alert to ObeyX: {message}")
    try:
        from obeyx_core.obeyx_interface import obeyx_alert
        obeyx_alert("context_engine", message)
    except ImportError:
        print("[⚠️] ObeyX interface not ready for alerts")

# ----------------------------------------
# إدارة الكاش (حفظ واسترجاع)

@safe_execute
def set_context_cache(key, value):
    context_cache[key] = value
    context_cache_timestamps[key] = time.time()

@safe_execute
def get_context_cache(key):
    if key in context_cache:
        age = time.time() - context_cache_timestamps.get(key, 0)
        if age < CACHE_EXPIRY_SECONDS:
            return context_cache[key]
        else:
            # حذف القيمة إذا انتهت صلاحيتها
            context_cache.pop(key, None)
            context_cache_timestamps.pop(key, None)
    return None

# ----------------------------------------
# إضافة بيانات جديدة للتحليل (تدفق البيانات)

@safe_execute
def enqueue_input(data):
    """
    إضافة بيانات إلى قائمة الانتظار لتحليل السياق
    """
    if input_queue.full():
        print("[⚠️] Input queue full. Dropping oldest item to enqueue new data.")
        try:
            _ = input_queue.get_nowait()  # إخراج أقدم عنصر
        except queue.Empty:
            pass
    input_queue.put(data)

# ----------------------------------------
# المعالجة الذكية الأساسية (محاكاة تحليل متعدد الطبقات)

@safe_execute
def analyze_context(data):
    """
    تحليل البيانات المقدمة وإرجاع استنتاجات أو أوامر ذكية.
    data: dict أو نص أو أي نوع من البيانات
    """
    # تجربة استرجاع كاش أولاً
    cache_key = str(data)
    cached_result = get_context_cache(cache_key)
    if cached_result:
        return cached_result

    # تحليل بسيط على سبيل المثال (يمكن تعقيدها)
    result = {
        "timestamp": str(datetime.now()),
        "input_summary": str(data)[:100],  # ملخص أول 100 حرف
        "analysis": None,
        "recommendation": None,
        "confidence": 0.0
    }

    # نوع التحليل بناءً على نوع الدخل
    if isinstance(data, dict):
        # تحليل بيانات JSON / الهياكل
        result["analysis"] = f"Analyzed dict with {len(data)} keys."
        result["recommendation"] = "Process according to schema."
        result["confidence"] = 0.85
    elif isinstance(data, str):
        # تحليل نصوص (مثلاً، أوامر صوتية أو نصوص)
        if "error" in data.lower():
            result["analysis"] = "Detected error-related context."
            result["recommendation"] = "Trigger diagnostic module."
            result["confidence"] = 0.95
        else:
            result["analysis"] = "General text analysis performed."
            result["recommendation"] = "Forward to NLP or assistant."
            result["confidence"] = 0.75
    else:
        # بيانات غير معروفة أو ملفات
        result["analysis"] = f"Received data of type {type(data).__name__}."
        result["recommendation"] = "Store for later deep analysis."
        result["confidence"] = 0.6

    # حفظ النتيجة في الكاش
    set_context_cache(cache_key, result)
    # تسجيل الحدث
    event_log.append({"time": datetime.now(), "data": data, "result": result})

    return result

# ----------------------------------------
# مراقبة قائمة الانتظار وتشغيل التحليل بشكل مستمر في خيط منفصل

def process_input_queue():
    while True:
        try:
            data = input_queue.get()
            if data is None:
                break
            analyze_context(data)
        except Exception as e:
            print(f"[❗] Error processing queue: {e}")
            traceback.print_exc()
        time.sleep(0.01)  # تخفيف الحمل قليلاً

def start_context_engine():
    print("[ContextEngine] 🚀 Starting context analysis engine...")
    threading.Thread(target=process_input_queue, daemon=True).start()

# ----------------------------------------
# دعم ملفات وأنواع متعددة (نماذج مبسطة)

@safe_execute
def read_file_content(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@safe_execute
def save_file_content(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True

# ----------------------------------------
# دعم استرجاع البيانات المحذوفة (مبسطة)

deleted_items = deque(maxlen=100)

@safe_execute
def backup_deleted_item(item):
    deleted_items.append(item)

@safe_execute
def recover_last_deleted():
    if deleted_items:
        return deleted_items.pop()
    return None

# ----------------------------------------
# اختبار وحدات (لوحدها)

if __name__ == "__main__":
    start_context_engine()
    print(analyze_context({"command": "فتح الملف", "file": "test.txt"}))
    enqueue_input("هذا نص للاختبار وتحليل السياق مع ObeyX")
    time.sleep(1)
    recovered = recover_last_deleted()
    print(f"Recovered deleted item: {recovered}")
