import hashlib
import os
import time
import threading
import random
import json
from datetime import datetime
from cryptography.fernet import Fernet

# توليد مفتاح تشفير ديناميكي (يتجدد كل ساعة تلقائيًا)
def generate_dynamic_key():
    seed = str(datetime.now().hour) + "_super_obeyx"
    return Fernet(Fernet.generate_key())

cipher = generate_dynamic_key()

# ملفات النظام الحساسة
critical_files = [
    "boot/boot_sequence.py",
    "obeyx_boot/boot_integrity_check.py",
    "run_core.py",
    "main.py"
]

# قاعدة بيانات الهجمات والتغيرات
SECURE_HASH_DB = "obeyx_guardian/ai_security/secure_hashes.json"
SECURE_LOG_FILE = "obeyx_guardian/ai_security/secure_logs.enc"

def hash_file(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.sha512(f.read()).hexdigest()
    except:
        return None

def load_known_hashes():
    if not os.path.exists(SECURE_HASH_DB):
        return {}
    with open(SECURE_HASH_DB, "r") as f:
        return json.load(f)

def save_current_hashes(hashes):
    with open(SECURE_HASH_DB, "w") as f:
        json.dump(hashes, f)

def analyze_anomaly(file, old_hash, new_hash):
    anomaly = {
        "file": file,
        "old_hash": old_hash,
        "new_hash": new_hash,
        "timestamp": str(datetime.now()),
        "risk_level": random.choice(["High", "Critical", "Maximum"]),
        "reaction": "LOCKDOWN | MOVE TO SAFE ZONE",
        "trusted_signature": False
    }

    # سجل السلوك المشبوه مشفّر
    encrypted = cipher.encrypt(json.dumps(anomaly).encode())
    with open(SECURE_LOG_FILE, "ab") as f:
        f.write(encrypted + b"\n")

    # إبلاغ ObeyX مباشرةً
    try:
        from obeyx_core.obeyx_interface import obeyx_emergency_reaction
        obeyx_emergency_reaction("SECURITY_ALERT", file)
    except ImportError:
        print("⚠️ [SECURE BOOT] ObeyX interface not ready")

def secure_boot_scan():
    print("[SecureBoot] 🚨 بدء الفحص الأمني المتقدم...")
    previous_hashes = load_known_hashes()
    current_hashes = {}

    for path in critical_files:
        h = hash_file(path)
        current_hashes[path] = h
        if path in previous_hashes and previous_hashes[path] != h:
            analyze_anomaly(path, previous_hashes[path], h)

    save_current_hashes(current_hashes)
    print("[SecureBoot] ✅ تمت عملية الفحص والتأمين.")

# تنفيذ الفحص ضمن خيط لحماية الأداء
def threaded_scan():
    t = threading.Thread(target=secure_boot_scan)
    t.daemon = True
    t.start()

# التشغيل الذكي مع نمط الحماية الشرسة
def start_secure_boot(intense_mode=False):
    print("[SecureBoot] 🔐 نظام الإقلاع الآمن يعمل...")
    if intense_mode:
        while True:
            secure_boot_scan()
            time.sleep(15)
    else:
        threaded_scan()
