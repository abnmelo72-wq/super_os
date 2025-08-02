import os
import hashlib
import json
import time
import datetime
import socket

CHECKSUM_FILE = "boot_fingerprints.json"
ERROR_LOG = "boot_errors.log"
REPORT_SERVER = "127.0.0.1"  # ضع عنوان مركز التقارير إذا كنت تستخدم وضع الاتصال

# ==========🔐 وظائف التحقق المتقدمة ==========
def calculate_hash(file_path):
    hashes = {
        "sha512": hashlib.sha512(),
        "sha3_512": hashlib.sha3_512(),
        "blake2b": hashlib.blake2b()
    }
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                for h in hashes.values():
                    h.update(chunk)
    except FileNotFoundError:
        return None
    return {k: v.hexdigest() for k, v in hashes.items()}

def load_fingerprints():
    if not os.path.exists(CHECKSUM_FILE):
        return {}
    with open(CHECKSUM_FILE, 'r') as f:
        return json.load(f)

def save_fingerprints(fingerprints):
    with open(CHECKSUM_FILE, 'w') as f:
        json.dump(fingerprints, f, indent=2)

def log_error(message):
    timestamp = datetime.datetime.now().isoformat()
    with open(ERROR_LOG, 'a') as log:
        log.write(f"[{timestamp}] {message}\n")

def send_report_to_server(data):
    try:
        # محاكاة إرسال تقرير للنظام المركزي
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((REPORT_SERVER, 5050))
            s.sendall(json.dumps(data).encode())
    except Exception as e:
        log_error(f"فشل الإرسال المركزي: {e}")

# ==========⚠️ التحقق الديناميكي ==========
def check_integrity():
    critical_files = [
        "kernel/kernel.bin",
        "boot/grub/grub.cfg",
        "init/system_init.py",
        "obeyx_core/obeyx_brain.py"
    ]

    fingerprints = load_fingerprints()
    changed = []

    for path in critical_files:
        current = calculate_hash(path)
        if not current:
            log_error(f"🔴 مفقود: {path}")
            changed.append({"file": path, "status": "missing"})
            continue

        previous = fingerprints.get(path)
        if previous != current:
            log_error(f"🟡 تغيّر الملف: {path}")
            changed.append({"file": path, "status": "modified", "current": current, "expected": previous})
        else:
            print(f"✅ الملف سليم: {path}")

    if changed:
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "warning",
            "changes": changed,
            "host": socket.gethostname()
        }
        send_report_to_server(report)
        return False
    return True

# ==========🛠️ الإصلاح الذاتي التجريبي ==========
def attempt_self_heal(changed_files):
    healed = []
    for item in changed_files:
        path = item["file"]
        if item["status"] == "missing":
            log_error(f"❌ لا يمكن ترميم الملف المفقود تلقائيًا: {path}")
        elif item["status"] == "modified":
            backup_path = path + ".bak"
            if os.path.exists(backup_path):
                os.replace(backup_path, path)
                log_error(f"🛠️ تمت استعادة نسخة احتياطية من {path}")
                healed.append(path)
            else:
                log_error(f"⚠️ لا يوجد نسخة احتياطية للملف {path}")
    return healed

# ==========🚀 بداية التحقق ==========
def run_boot_check():
    print("🚨 بدأ التحقق من سلامة الإقلاع لنظام ObeyX...")
    result = check_integrity()
    if not result:
        print("⚠️ تم الكشف عن مشاكل! محاولة الإصلاح...")
        changed_files = load_latest_changes()
        healed = attempt_self_heal(changed_files)
        if healed:
            print(f"✅ تم إصلاح {len(healed)} ملف(ات) تلقائيًا.")
        else:
            print("❌ فشل الإصلاح التلقائي. تحقق يدوي مطلوب.")
    else:
        print("🟢 التمهيد سليم. كل شيء تحت السيطرة.")

def load_latest_changes():
    # تحميل آخر تغييرات محفوظة بالتقرير الأخير
    if not os.path.exists(ERROR_LOG):
        return []
    changes = []
    with open(ERROR_LOG, 'r') as log:
        lines = log.readlines()[-20:]
        for line in lines:
            if "تغيّر الملف" in line or "مفقود" in line:
                parts = line.split(": ")
                if len(parts) == 2:
                    changes.append({"file": parts[1].strip(), "status": "modified" if "تغيّر" in line else "missing"})
    return changes

# ==========✅ حفظ البصمات ==========
def store_current_state():
    print("🧬 حفظ حالة النظام الحالية...")
    critical_files = [
        "kernel/kernel.bin",
        "boot/grub/grub.cfg",
        "init/system_init.py",
        "obeyx_core/obeyx_brain.py"
    ]
    current_fingerprints = {}
    for path in critical_files:
        h = calculate_hash(path)
        if h:
            current_fingerprints[path] = h
    save_fingerprints(current_fingerprints)
    print("✅ تم حفظ البصمات.")

# ==========🔰 نقطة التشغيل ==========
if __name__ == "__main__":
    run_boot_check()
