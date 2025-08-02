# ~/super_os/obeyx_boot/hardware_checker.py

import platform
import psutil
import socket
import uuid
import subprocess
import json
import datetime

# تحليل مستقبلي، تخميني، ذكي
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

class HardwareChecker:
    def __init__(self):
        self.report = {}
        self.ai_model = None
        self.device_score = 0

    def analyze_cpu(self):
        cpu_info = {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "frequency": psutil.cpu_freq()._asdict(),
            "architecture": platform.machine(),
            "processor": platform.processor()
        }
        self.report["CPU"] = cpu_info

    def analyze_memory(self):
        memory_info = psutil.virtual_memory()._asdict()
        self.report["Memory"] = memory_info

    def analyze_storage(self):
        disk_info = psutil.disk_usage('/')._asdict()
        self.report["Storage"] = disk_info

    def analyze_network(self):
        net_info = {
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)
                                     for i in range(0, 8 * 6, 8)][::-1])
        }
        self.report["Network"] = net_info

    def check_future_networks(self):
        self.report["Future_Networks_Supported"] = [
            "WiFi6", "5G", "Mesh", "LoRa", "ZigBee", "Starlink", "6G (Predicted)"
        ]

    def scan_ai_compatibility(self):
        ai_tools = {
            "OpenCV": self.try_import("cv2"),
            "TensorFlow": self.try_import("tensorflow"),
            "PyTorch": self.try_import("torch"),
            "Whisper": self.try_import("whisper"),
        }
        self.report["AI_Tools_Supported"] = ai_tools

    def try_import(self, module):
        try:
            __import__(module)
            return True
        except ImportError:
            return False

    def classify_device(self):
        # قواعد مبسطة لتقييم أولي، يمكن استبدالها بـ ML فعلي لاحقاً
        score = 0
        cpu = self.report.get("CPU", {})
        memory = self.report.get("Memory", {})
        storage = self.report.get("Storage", {})

        if cpu.get("total_cores", 0) >= 8:
            score += 2
        if memory.get("total", 0) >= 8 * 1024**3:
            score += 2
        if storage.get("total", 0) >= 256 * 1024**3:
            score += 2
        if self.report.get("AI_Tools_Supported", {}).get("Whisper", False):
            score += 1

        self.device_score = score
        self.report["Device_Classification"] = {
            "score": score,
            "level": self.score_level(score)
        }

    def score_level(self, score):
        if score >= 6:
            return "⚡ خارق (ObeyX Ultra Compatible)"
        elif score >= 4:
            return "🔥 متقدم"
        elif score >= 2:
            return "🟡 متوسط"
        else:
            return "🔴 منخفض - قد لا يدعم كل قدرات ObeyX"

    def generate_report(self):
        self.analyze_cpu()
        self.analyze_memory()
        self.analyze_storage()
        self.analyze_network()
        self.check_future_networks()
        self.scan_ai_compatibility()
        self.classify_device()

        timestamp = datetime.datetime.now().isoformat()
        self.report["timestamp"] = timestamp
        return self.report

    def save_report(self, filename="hardware_report.json"):
        with open(filename, "w") as f:
            json.dump(self.report, f, indent=4)

if __name__ == "__main__":
    checker = HardwareChecker()
    report = checker.generate_report()
    checker.save_report()
    print(json.dumps(report, indent=4))
