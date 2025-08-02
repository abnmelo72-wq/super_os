import shutil
import os
import platform
import subprocess
import socket
import json
import psutil

from core.obeyx_boot.utils.smart_boot_utils import SmartBootUtils

report = SmartBootUtils.dump_report_to_json()
print(f"📦 تقرير النظام محفوظ في: {report}")

class SmartBootUtils:

    @staticmethod
    def check_disk_space(path="/"):
        total, used, free = shutil.disk_usage(path)
        return {
            "total_gb": round(total / (2**30), 2),
            "used_gb": round(used / (2**30), 2),
            "free_gb": round(free / (2**30), 2)
        }

    @staticmethod
    def detect_os():
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "is_wsl": 'microsoft' in platform.uname().release.lower(),
            "is_vm": SmartBootUtils.is_virtual_machine()
        }

    @staticmethod
    def is_virtual_machine():
        try:
            with open('/sys/class/dmi/id/product_name') as f:
                product = f.read().lower()
                return 'virtual' in product or 'vmware' in product or 'qemu' in product
        except:
            return False

    @staticmethod
    def verify_environment(commands=None):
        if commands is None:
            commands = ["python3", "ffmpeg", "curl", "git"]
        return {cmd: shutil.which(cmd) is not None for cmd in commands}

    @staticmethod
    def system_summary():
        return {
            "cpu": platform.processor(),
            "cpu_cores": psutil.cpu_count(logical=False),
            "cpu_threads": psutil.cpu_count(logical=True),
            "freq_ghz": round(psutil.cpu_freq().current / 1000, 2),
            "ram_gb": round(psutil.virtual_memory().total / (2**30), 2),
            "machine": platform.machine(),
            "arch": platform.architecture()[0],
            "platform": platform.platform(),
            "node": platform.node(),
            "battery": SmartBootUtils.get_battery_status()
        }

    @staticmethod
    def get_battery_status():
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "plugged": battery.power_plugged
            }
        return "Not available"

    @staticmethod
    def is_inside_container():
        try:
            with open("/proc/1/cgroup") as f:
                return any("docker" in line or "lxc" in line for line in f)
        except:
            return False

    @staticmethod
    def is_root():
        return os.geteuid() == 0

    @staticmethod
    def get_ip_info():
        ip = socket.gethostbyname(socket.gethostname())
        try:
            external_ip = subprocess.getoutput("curl -s ifconfig.me")
        except:
            external_ip = "unknown"
        return {
            "local_ip": ip,
            "external_ip": external_ip
        }

    @staticmethod
    def check_security_files():
        critical = ["/etc/passwd", "/etc/shadow", "/etc/sudoers"]
        results = {}
        for file in critical:
            try:
                stat = os.stat(file)
                results[file] = {
                    "exists": True,
                    "mode": oct(stat.st_mode)[-3:],
                    "owner": stat.st_uid
                }
            except:
                results[file] = {"exists": False}
        return results

    @staticmethod
    def dump_report_to_json(path="/tmp/system_report.json"):
        report = {
            "disk": SmartBootUtils.check_disk_space(),
            "os": SmartBootUtils.detect_os(),
            "summary": SmartBootUtils.system_summary(),
            "env": SmartBootUtils.verify_environment(),
            "security": SmartBootUtils.check_security_files(),
            "network": SmartBootUtils.get_ip_info(),
            "is_root": SmartBootUtils.is_root()
        }
        with open(path, "w") as f:
            json.dump(report, f, indent=4)
        return path
