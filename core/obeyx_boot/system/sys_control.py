import os
import platform
import subprocess
import psutil
import time
from datetime import datetime
from ..utils.boot_logger import BootLogger

logger = BootLogger()

class SystemController:
    def __init__(self):
        self.system = platform.system()
        self.node = platform.node()
        self.architecture = platform.machine()
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
        logger.log(f"[🧠SystemController] initialized on {self.system} - Node: {self.node} - Arch: {self.architecture}")

    # ⛔️ إيقاف الجهاز بذكاء
    def shutdown(self):
        logger.warning("🔻 Intelligent shutdown initiated...")
        if self.confirm_action("Are you sure you want to shutdown?"):
            self._secure_log_state()
            self._run_os_command("shutdown")
        else:
            logger.log("❎ Shutdown cancelled by user.")

    # 🔁 إعادة تشغيل
    def restart(self):
        logger.warning("🔄 Intelligent restart initiated...")
        if self.confirm_action("Restart system?"):
            self._secure_log_state()
            self._run_os_command("restart")
        else:
            logger.log("❎ Restart cancelled by user.")

    # 🦺 وضع الأمان
    def enter_safe_mode(self):
        logger.log("🟡 Entering smart safe mode (stub)...")
        logger.warning("⚠️ Safe mode is a work-in-progress and not implemented yet!")

    # 🧮 استخدام القرص
    def check_disk_usage(self):
        logger.log("🧮 Checking disk usage...")
        usage = psutil.disk_usage('/')
        logger.log(f"Total: {usage.total // (1024 ** 3)} GB")
        logger.log(f"Used: {usage.used // (1024 ** 3)} GB")
        logger.log(f"Free: {usage.free // (1024 ** 3)} GB")
        logger.log(f"Percentage: {usage.percent}%")

    # 🧠 حالة المعالج والذاكرة
    def system_status(self):
        logger.log("📊 Smart system status report:")
        logger.log(f"🕒 Uptime: {self.get_uptime()}")
        logger.log(f"🧠 CPU usage: {psutil.cpu_percent()}%")
        logger.log(f"🧠 Memory usage: {psutil.virtual_memory().percent}%")
        logger.log(f"🖴 Disk usage: {psutil.disk_usage('/').percent}%")

    # 🔐 تحقق ذكي من النظام
    def is_virtualized(self):
        logger.log("🔎 Checking for virtualization...")
        output = subprocess.getoutput("systemd-detect-virt")
        if output != "none":
            logger.warning(f"⚠️ Virtualization detected: {output}")
            return True
        return False

    # 📁 قائمة العمليات النشطة
    def list_processes(self, limit=10):
        logger.log(f"🔬 Top {limit} active processes:")
        procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)
        for proc in procs[:limit]:
            logger.log(f"PID: {proc.info['pid']} - {proc.info['name']} - CPU: {proc.info['cpu_percent']}%")

    # 📜 سجل التحقق الذكي قبل تنفيذ الأوامر
    def confirm_action(self, prompt):
        response = input(f"{prompt} [y/N]: ").strip().lower()
        return response == "y"

    # 🔄 تنفيذ أوامر النظام الذكية
    def _run_os_command(self, command):
        if self.system == "Linux":
            if command == "shutdown":
                os.system("shutdown now")
            elif command == "restart":
                os.system("reboot")
        elif self.system == "Windows":
            if command == "shutdown":
                os.system("shutdown /s /t 0")
            elif command == "restart":
                os.system("shutdown /r /t 0")
        else:
            logger.error("Unsupported OS for command")

    # 🔐 تسجيل الحالة قبل تنفيذ العمليات الخطيرة
    def _secure_log_state(self):
        logger.log("📁 Saving current system state...")
        try:
            with open("/tmp/system_state.log", "w") as f:
                f.write(f"Boot Time: {self.boot_time}\n")
                f.write(f"CPU Usage: {psutil.cpu_percent()}%\n")
                f.write(f"Memory Usage: {psutil.virtual_memory().percent}%\n")
                f.write(f"Disk Usage: {psutil.disk_usage('/').percent}%\n")
        except Exception as e:
            logger.error(f"Failed to save system state: {e}")

    # ⌛️ وقت التشغيل
    def get_uptime(self):
        uptime_sec = time.time() - psutil.boot_time()
        uptime_hr = uptime_sec / 3600
        return f"{uptime_hr:.2f} hours"
