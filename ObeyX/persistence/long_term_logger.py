# persistence/long_term_logger.py
import os
import json
import hashlib
import datetime
import threading
import random

# مسار التخزين
STORAGE_PATH = "persistence/memcore_data"

# إنشاء المسار إذا غير موجود
os.makedirs(STORAGE_PATH, exist_ok=True)

# ذاكرة طويلة الأمد - ذاكرة عصبية متكاملة
memory_graph = {}

# إعدادات التخزين
SAVE_INTERVAL = 30  # ثوانٍ بين كل تخزين تلقائي

# دعم استعادة المحذوف والتعويض
recovery_bin = {}

# دعم تحليل أي نوع بيانات
SUPPORTED_TYPES = ["text", "code", "audio", "image", "event", "thought", "behavior"]

# تشفير بسيط باستخدام SHA256 لتأمين الهوية
def secure_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# تسجيل إدخال جديد
def log_entry(entry_type, content, tags=[], metadata={}):
    if entry_type not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported type: {entry_type}")

    timestamp = datetime.datetime.utcnow().isoformat()
    entry_id = secure_hash(f"{entry_type}_{timestamp}_{random.random()}")

    entry = {
        "id": entry_id,
        "type": entry_type,
        "content": content,
        "tags": tags,
        "metadata": metadata,
        "timestamp": timestamp,
        "deleted": False
    }

    memory_graph[entry_id] = entry
    print(f"[🧠 LongMemory] Logged entry: {entry_type} → {entry_id}")
    return entry_id

# حذف آمن مع دعم الاسترجاع
def soft_delete(entry_id):
    if entry_id in memory_graph:
        memory_graph[entry_id]["deleted"] = True
        recovery_bin[entry_id] = memory_graph[entry_id]
        print(f"[🧠 LongMemory] Entry {entry_id} moved to recovery bin.")

# استعادة المحذوف
def restore_entry(entry_id):
    if entry_id in recovery_bin:
        memory_graph[entry_id] = recovery_bin.pop(entry_id)
        memory_graph[entry_id]["deleted"] = False
        print(f"[🧠 LongMemory] Entry {entry_id} restored.")

# البحث في الذاكرة
def search_memory(keyword):
    results = []
    for entry in memory_graph.values():
        if not entry["deleted"] and (keyword in entry["content"] or keyword in entry.get("tags", [])):
            results.append(entry)
    return results

# الحفظ الدوري التلقائي
def auto_save_loop():
    while True:
        save_memory()
        time.sleep(SAVE_INTERVAL)

# حفظ الذاكرة إلى ملف
def save_memory():
    path = os.path.join(STORAGE_PATH, "long_term_memory.json")
    with open(path, "w") as f:
        json.dump(memory_graph, f, indent=2)
    print(f"[💾 LongMemory] Memory saved to {path}")

# تحميل الذاكرة
def load_memory():
    global memory_graph
    path = os.path.join(STORAGE_PATH, "long_term_memory.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            memory_graph = json.load(f)
        print(f"[🔁 LongMemory] Loaded memory from {path}")
    else:
        print("[🔁 LongMemory] No previous memory found.")

# بدء الذاكرة الذكية
def start_memory_engine():
    print("[🚀 LongMemory] Starting long-term memory engine...")
    load_memory()
    t = threading.Thread(target=auto_save_loop, daemon=True)
    t.start()

# مثال استخدام أولي (يمكن إزالة)
if __name__ == "__main__":
    start_memory_engine()
    log_entry("text", "بدأ نظام Super OS الذكي التخزين طويل الأمد", tags=["start", "super_os", "init"])
    log_entry("code", "def example(): return True", tags=["code", "example"])
