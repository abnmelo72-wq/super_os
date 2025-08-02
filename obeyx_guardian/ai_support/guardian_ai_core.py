# guardian_ai_core.py ⚔️
# وحدة حماية شاملة فائقة الذكاء والأمان

import os
import time
import hashlib
from datetime import datetime

class GuardianAICore:
    def __init__(self, monitored_paths, protection_level="medium"):
        self.monitored_paths = monitored_paths
        self.protection_level = protection_level  # low, medium, high, military
        self.threat_keywords = [
            "delete", "format", "shutdown", "kill", "rm -rf", "mkfs", "dd if=",
            "malware", "attack", "exploit", "zero-day", "forkbomb", "chmod 777 -R /"
        ]
        self.history_log = "/var/log/obeyx/guardian_ai_history.json"
        self.report_log = "/var/log/obeyx/guardian_ai_report.log"
        self.threat_count = 0

    # =====================
    # 🔒 التكامل متعدد الأبعاد
    # =====================
    def fingerprint(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                content_hash = hashlib.sha512(f.read()).hexdigest()
            size = os.path.getsize(file_path)
            mtime = os.path.getmtime(file_path)
            permissions = oct(os.stat(file_path).st_mode)[-3:]
            return {
                "hash": content_hash,
                "size": size,
                "mtime": mtime,
                "permissions": permissions
            }
        except FileNotFoundError:
            return None

    def analyze_integrity(self):
        results = []
        for path in self.monitored_paths:
            if not os.path.exists(path):
                results.append((path, "🛑 مفقود", None))
            else:
                fp = self.fingerprint(path)
                status = f"✅ موجود | الحجم: {fp['size']}B | إذن: {fp['permissions']} | توقيت: {time.ctime(fp['mtime'])}"
                results.append((path, status, fp))
        return results

    def log_report(self, report):
        os.makedirs(os.path.dirname(self.report_log), exist_ok=True)
        with open(self.report_log, "a") as f:
            now = datetime.now().isoformat()
            f.write(f"\n[{now}] 🧠 Guardian AI Report\n")
            for path, status, _ in report:
                f.write(f"{path}: {status}\n")

    # =====================
    # 🧠 تحليل الأوامر مع تقييم التهديد
    # =====================
    def analyze_threats_in_command(self, command_text):
        detected = []
        for threat in self.threat_keywords:
            if threat in command_text.lower():
                severity = self.estimate_threat_level(threat)
                detected.append((threat, severity))
        return detected

    def estimate_threat_level(self, keyword):
        high_threats = ["rm -rf", "mkfs", "dd if=", "shutdown", "forkbomb"]
        medium_threats = ["chmod 777", "attack", "malware", "exploit"]
        return "🔥 عالي" if keyword in high_threats else "⚠️ متوسط" if keyword in medium_threats else "🔎 منخفض"

    def guardian_decision(self, detected_threats):
        if not detected_threats:
            return "safe", "✅ لا تهديدات"
        else:
            self.threat_count += len(detected_threats)
            threats_list = ", ".join([f"{t[0]} ({t[1]})" for t in detected_threats])
            action = "🔐 منع" if self.protection_level in ["high", "military"] else "⚠️ تحذير"
            return action, f"تم رصد تهديدات: {threats_list}"

     def guardian_protect(self, command_text):
        threats = self.analyze_threats_in_command(command_text)
        decision, message = self.guardian_decision(threats)
        return {
            "status": decision,
            "message": message,
            "threats": threats,
            "level": self.protection_level
        }

    # =====================
    # 🔁 المراقبة الحية (Live Watch)
    # =====================
    def live_watch(self, interval=5):
        last_states = {p: self.fingerprint(p) for p in self.monitored_paths}
        print("📡 بدء المراقبة الحية...")
        while True:
            time.sleep(interval)
            for path in self.monitored_paths:
                new_state = self.fingerprint(path)
                if new_state != last_states.get(path):
                    now = datetime.now().isoformat()
                    print(f"[{now}] ⚠️ تغير في {path}")
                    self.log_report([(path, "🔁 تغير تم رصده", new_state)])
                    last_states[path] = new_state

    # =====================
    # 🧪 المحاكاة (Simulation)
    # =====================
    def simulate_threat_response(self, command_text):
        print("🔬 اختبار الذكاء الحارس...")
        result = self.guardian_protect(command_text)
        print("🧪 نتيجة المحاكاة:")
        for k, v in result.items():
            print(f"{k}: {v}")
        return result


def start_guardian():
    paths = [
        "/system/core/kernel.bin",
        "/ai_core/main_ai_brain.py",
        "/obeyx_boot/boot_sequence.py",
        "/obeyx_boot/boot_integrity_check.py",
    ]
    guardian = GuardianAICore(paths, protection_level="military")
    integrity = guardian.analyze_integrity()
    guardian.log_report(integrity)
    print("✅ Guardian AI Activated: Integrity check done.")
# =====================
# 🧪 مثال استخدام حي
# =====================
if __name__ == "__main__":
    paths = [
        "/system/core/kernel.bin",
        "/ai_core/main_ai_brain.py",
        "/obeyx_boot/boot_sequence.py",
        "/obeyx_boot/boot_integrity_check.py",
    ]

    guardian = GuardianAICore(paths, protection_level="military")

    # فحص الملفات
    integrity = guardian.analyze_integrity()
    guardian.log_report(integrity)
    print("✅ تحليل التكامل مكتمل")

    # اختبار تهديد نصي
    guardian.simulate_threat_response("sudo rm -rf / --no-preserve-root")

    # يمكنك تجربة المراقبة الحية عبر:
    # guardian.live_watch(interval=10)
