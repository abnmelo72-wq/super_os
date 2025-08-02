# safe_mode.py - Super OS Safe Mode Handler v2.0 - Powered by ObeyX

import os
import time
import platform
import subprocess
import logging
from datetime import datetime

# المسارات الافتراضية
LOG_FILE = "/var/log/super_os/safe_mode.log"
RECOVERY_SCRIPT = "/super_os/recovery/recover_system.py"
AI_ANALYZER_SCRIPT = "/super_os/ai_core/boot_ai_analyzer.py"

# إعداد التسجيل
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# وظائف الذكاء الصناعي الذكي المتقدمة
class SafeMode:
    def __init__(self):
        self.system_info = self.get_system_info()
        self.issue_detected = False
        self.reason = "غير معروف"
        self.entered_by_user = False

    def get_system_info(self):
        return {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }

    def detect_ai_threat_patterns(self):
        # TODO: التكامل مع وحدة تحليل سلوك المستخدم
        suspicious_logs = ["/var/log/syslog", "/var/log/auth.log"]
        threats = []
        for log_path in suspicious_logs:
            if os.path.exists(log_path):
                with open(log_path, "r") as log_file:
                    lines = log_file.readlines()[-200:]
                    for line in lines:
                        if "unauthorized" in line.lower() or "failure" in line.lower():
                            threats.append(line.strip())
        return threats

    def analyze_previous_boots(self):
        # تحليل مشاكل الإقلاع السابقة
        boot_log = "/var/log/boot.log"
        report = []
        if os.path.exists(boot_log):
            with open(boot_log, "r") as bl:
                report = [line for line in bl if "fail" in line.lower()]
        return report

    def enter_safe_mode(self, reason="غير معروف", auto=False):
        self.reason = reason
        self.issue_detected = True
        logging.warning(f"[SAFE_MODE] دخول الوضع الآمن بسبب: {reason} | آلي: {auto}")
        print(f"⚠️ تم تفعيل الوضع الآمن. السبب: {reason}")

        if os.path.exists(AI_ANALYZER_SCRIPT):
            print("📡 تشغيل وحدة تحليل الذكاء الصناعي...")
            subprocess.call(["python3", AI_ANALYZER_SCRIPT])

        print("🧠 تشغيل ObeyX لمساعدتك...")
        time.sleep(1)
        self.launch_obeyx_helper()

    def launch_obeyx_helper(self):
        print("""
        🤖 أهلاً بك في الوضع الآمن - Super OS
        مساعدك الذكي ObeyX معك الآن!
        1. تشخيص الأعطال
        2. استعادة نقطة سابقة
        3. فحص العتاد
        4. تصفح النظام بسلام
        """)
        # لاحقاً: دعم الأوامر الصوتية لتفعيل الخيارات

    def check_and_trigger(self):
        ai_threats = self.detect_ai_threat_patterns()
        boot_issues = self.analyze_previous_boots()

        if ai_threats:
            self.enter_safe_mode(reason="تهديدات أمنية مشبوهة تم كشفها.", auto=True)
        elif boot_issues:
            self.enter_safe_mode(reason="مشاكل سابقة في الإقلاع تم اكتشافها.", auto=True)
        else:
            print("✅ لم يتم اكتشاف مشاكل خطيرة. النظام يعمل بوضعه الطبيعي.")

    def manual_entry(self):
        self.entered_by_user = True
        self.enter_safe_mode(reason="تم التفعيل من قبل المستخدم.", auto=False)

    def run_recovery_if_needed(self):
        if self.issue_detected and os.path.exists(RECOVERY_SCRIPT):
            subprocess.call(["python3", RECOVERY_SCRIPT])

# نقطة الدخول
if __name__ == "__main__":
    sm = SafeMode()
    
    # لاحقًا: استخدم تحليل صوت المستخدم لتفعيل الوضع الآمن بصوت معين
    user_input = input("🔒 هل تريد الدخول إلى الوضع الآمن؟ (y/n): ").strip().lower()
    if user_input == 'y':
        sm.manual_entry()
    else:
        sm.check_and_trigger()

    sm.run_recovery_if_needed()
