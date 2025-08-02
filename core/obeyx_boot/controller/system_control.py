import os
import platform
import subprocess
import psutil
import time
import logging

class SystemController:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.log_file = "/tmp/obeyx_system_control.log"
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)

    def log(self, message):
        print(f"[📌 SYSTEM]: {message}")
        logging.info(message)

    def shutdown(self):
        self.log("🔻 إيقاف تشغيل النظام...")
        try:
            if self.os_type == "linux":
                os.system("poweroff")
            elif self.os_type == "windows":
                os.system("shutdown /s /t 1")
            elif self.os_type == "android":
                os.system("reboot -p")
            else:
                self.log("⚠️ نظام غير مدعوم")
        except Exception as e:
            self.log(f"❌ فشل الإيقاف: {e}")

    def reboot(self):
        self.log("🔁 إعادة تشغيل النظام...")
        try:
            if self.os_type == "linux":
                os.system("reboot")
            elif self.os_type == "windows":
                os.system("shutdown /r /t 1")
            elif self.os_type == "android":
                os.system("reboot")
            else:
                self.log("⚠️ نظام غير مدعوم")
        except Exception as e:
            self.log(f"❌ فشل إعادة التشغيل: {e}")

    def get_system_info(self):
        self.log("📊 استعلام عن معلومات النظام...")
        try:
            info = {
                "OS": platform.system(),
                "Version": platform.version(),
                "CPU": platform.processor(),
                "Architecture": platform.machine(),
                "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
                "Uptime": f"{round(time.time() - psutil.boot_time()) // 60} minutes"
            }
            return info
        except Exception as e:
            self.log(f"❌ فشل الحصول على معلومات النظام: {e}")
            return {}

    def list_processes(self, limit=10):
        self.log(f"📋 عرض أول {limit} عمليات في النظام...")
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                processes.append(proc.info)
            sorted_procs = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
            return sorted_procs[:limit]
        except Exception as e:
            self.log(f"❌ فشل في جلب العمليات: {e}")
            return []

    def kill_process(self, pid):
        self.log(f"❌ محاولة إنهاء العملية PID: {pid}")
        try:
            p = psutil.Process(pid)
            p.terminate()
            self.log(f"✅ تم إنهاء العملية {pid}")
        except Exception as e:
            self.log(f"❌ فشل إنهاء العملية: {e}")

    def adjust_performance(self, mode="balanced"):
        self.log(f"⚙️ تعديل وضع الأداء إلى: {mode}")
        try:
            if mode == "high":
                os.system("cpupower frequency-set -g performance")
            elif mode == "low":
                os.system("cpupower frequency-set -g powersave")
            elif mode == "balanced":
                os.system("cpupower frequency-set -g ondemand")
            else:
                self.log("⚠️ وضع غير معروف")
        except Exception as e:
            self.log(f"❌ فشل ضبط الأداء: {e}")

    def monitor_resources(self):
        self.log("📈 مراقبة الموارد...")
        try:
            usage = {
                "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
                "RAM Usage": f"{psutil.virtual_memory().percent}%",
                "Disk Usage": f"{psutil.disk_usage('/').percent}%"
            }
            return usage
        except Exception as e:
            self.log(f"❌ فشل في مراقبة الموارد: {e}")
            return {}

    def open_app(self, app_name):
        self.log(f"🚀 محاولة تشغيل التطبيق: {app_name}")
        try:
            if self.os_type == "linux":
                subprocess.Popen([app_name])
            elif self.os_type == "windows":
                os.startfile(app_name)
            else:
                self.log("⚠️ التشغيل غير مدعوم على هذا النظام")
        except Exception as e:
            self.log(f"❌ فشل تشغيل التطبيق: {e}")
