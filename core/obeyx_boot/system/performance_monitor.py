# core/obeyx_boot/system/performance_monitor.py

import psutil
import time
import threading
import json
import datetime
from ..utils.boot_logger import BootLogger

logger = BootLogger()

class PerformanceMonitor:
    def __init__(self):
        self.alert_thresholds = {
            "cpu": 85,
            "memory": 90,
            "disk": 90,
            "temp": 75  # درجة حرارة وهمية إن لم تتوفر
        }
        logger.log("🧠 Smart PerformanceMonitor initialized with intelligent thresholds.")

    def get_cpu_usage(self):
        usage = psutil.cpu_percent(interval=1)
        logger.log(f"⚙️ CPU Usage: {usage}%")
        return usage

    def get_memory_usage(self):
        mem = psutil.virtual_memory()
        usage = mem.percent
        logger.log(f"🧠 Memory Usage: {usage}%")
        return usage

    def get_disk_usage(self):
        usage = psutil.disk_usage('/').percent
        logger.log(f"💽 Disk Usage: {usage}%")
        return usage

    def get_temperature(self):
        try:
            temps = psutil.sensors_temperatures()
            for name, entries in temps.items():
                for entry in entries:
                    logger.log(f"🔥 Temperature [{name}]: {entry.current}°C")
                    return entry.current
        except Exception:
            logger.log("🌡️ Temperature sensors not available.")
        return 0  # وهمي إن لم تتوفر

    def get_network_usage(self):
        counters = psutil.net_io_counters()
        logger.log(f"🌐 Network: Sent = {counters.bytes_sent} B, Received = {counters.bytes_recv} B")
        return counters.bytes_sent, counters.bytes_recv

    def get_top_processes(self, limit=5):
        processes = [(p.info['cpu_percent'], p.info['memory_percent'], p.info['name']) 
                     for p in psutil.process_iter(['cpu_percent', 'memory_percent', 'name'])]
        top = sorted(processes, key=lambda x: (x[0] + x[1]), reverse=True)[:limit]
        for proc in top:
            logger.log(f"📊 Top Process: {proc[2]} | CPU: {proc[0]}% | RAM: {proc[1]}%")
        return top

    def export_status(self, data):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"/tmp/performance_report_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        logger.log(f"📁 Status exported to {filepath}")

    def analyze_and_alert(self, data):
        alerts = []
        for key, val in data.items():
            if key in self.alert_thresholds and val >= self.alert_thresholds[key]:
                alerts.append(f"⚠️ {key.upper()} usage high: {val}%")
        if alerts:
            logger.log("🚨 ALERTS DETECTED!")
            for alert in alerts:
                logger.log(alert)

    def log_system_status(self):
        data = {
            "cpu": self.get_cpu_usage(),
            "memory": self.get_memory_usage(),
            "disk": self.get_disk_usage(),
            "temperature": self.get_temperature(),
            "network_sent_recv": self.get_network_usage(),
            "timestamp": str(datetime.datetime.now())
        }
        self.get_top_processes()
        self.analyze_and_alert(data)
        self.export_status(data)

    def monitor_loop(self, interval=5):
        logger.log("🔁 Starting smart performance monitor loop.")
        while True:
            try:
                self.log_system_status()
                time.sleep(interval)
            except Exception as e:
                logger.log(f"❌ Monitoring Error: {e}")
