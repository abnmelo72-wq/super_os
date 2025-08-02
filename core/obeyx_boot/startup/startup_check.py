from boot_logger import BootLogger
from boot_utils import BootUtils
from session_manager import SessionManager

class StartupCheck:
    def __init__(self):
        self.logger = BootLogger()
        self.utils = BootUtils()
        self.session = SessionManager()

    def run_all_checks(self):
        self.logger.smart_log("Startup", "✅ Starting full system checks")

        disk = self.utils.check_disk_space()
        self.logger.smart_log("Disk", f"Free: {disk['free_gb']} GB / Total: {disk['total_gb']} GB")

        env = self.utils.verify_environment()
        for k, v in env.items():
            self.logger.smart_log("Env", f"{k}: {'OK' if v else 'Missing'}")

        os_info = self.utils.detect_os()
        self.logger.smart_log("OS", f"{os_info['system']} {os_info['release']}")

        summary = self.utils.system_summary()
        self.logger.smart_log("System", f"{summary}")

        if self.utils.is_inside_container():
            self.logger.smart_log("Container", "Running inside containerized environment")

        self.session.save()
        self.logger.smart_log("Session", f"Session saved: {self.session.session_id}")

    def run_silent(self):
        try:
            self.run_all_checks()
        except Exception as e:
            self.logger.smart_log("Startup", f"Startup failed: {e}", level=40)
