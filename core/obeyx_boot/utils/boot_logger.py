# core/obeyx_boot/utils/boot_logger.py

import os
import datetime
import json

class BootLogger:
    def __init__(self, log_dir="/var/log/super_os"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "boot.log")
        self.errors_file = os.path.join(log_dir, "boot_errors.json")

    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().isoformat()
        entry = f"[{timestamp}] [{level}] {message}\n"
        with open(self.log_file, "a") as f:
            f.write(entry)

        # Log errors in JSON format separately
        if level == "ERROR":
            self._log_error_json(message, timestamp)

    def _log_error_json(self, message, timestamp):
        data = {"timestamp": timestamp, "error": message}
        if os.path.exists(self.errors_file):
            with open(self.errors_file, "r") as f:
                errors = json.load(f)
        else:
            errors = []

        errors.append(data)
        with open(self.errors_file, "w") as f:
            json.dump(errors, f, indent=2)

    def success(self, message):
        self.log(message, level="SUCCESS")

    def warning(self, message):
        self.log(message, level="WARNING")

    def error(self, message):
        self.log(message, level="ERROR")

    def print_last_entries(self, count=10):
        try:
            with open(self.log_file, "r") as f:
                lines = f.readlines()
                for line in lines[-count:]:
                    print(line.strip())
        except Exception as e:
            print(f"[BootLogger] Failed to read logs: {e}")
