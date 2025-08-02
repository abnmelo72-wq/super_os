# obeyx_guardian/thermal/ai_thermal_controller.py

import psutil
import time
import threading
import json
from datetime import datetime
import random

thermal_log = []

# حدود حرارية لكل مكوّن (قابلة للتحديث ديناميكيًا)
LIMITS = {
    "CPU": 75,
    "GPU": 80,
    "RAM": 90,
    "BATTERY": 45
}

# بيانات أولية للبروفايل (ObeyX قد يحدّثها)
user_profile = {
    "type": "designer_gamer",  # يمكن later نعمل auto-detect
    "tolerance": "high",       # low / medium / high
    "prefer_performance": True
}

# استخراج درجة حرارة CPU
def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                if "cpu" in entry.label.lower() or "core" in entry.label.lower():
                    return entry.current
    except:
        return None

# 🔍 قراءة GPU (مبدئيًا placeholder)
def get_gpu_temp():
    try:
        # نضيف دعم Nvidia أو AMD مستقبلاً
        return random.randint(40, 75)  # وهمي حاليًا
    except:
        return None

# RAM Usage
def get_ram_usage():
    try:
        mem = psutil.virtual_memory()
        return mem.percent
    except:
        return None

# Battery temp (إن وُجدت)
def get_battery_temp():
    try:
        battery = psutil.sensors_battery()
        if battery and hasattr(battery, 'temperature'):
            return battery.temperature
        return random.randint(30, 45)  # تخمين
    except:
        return None

# قراءة سرعة المراوح (لاحقًا نضيف دعم فعلي)
def get_fan_status():
    try:
        fans = psutil.sensors_fans()
        return fans
    except:
        return {}

# القرار الذكي لكل حالة
def smart_react(component, value):
    limit = LIMITS.get(component.upper(), 100)
    if value >= limit:
        action = None
        if user_profile["tolerance"] == "high":
            action = "adjust_framerate"
        elif user_profile["tolerance"] == "medium":
            action = "scale_resolution"
        else:
            action = "limit_cpu_threads"

        report = {
            "time": str(datetime.now()),
            "component": component,
            "value": value,
            "action": action,
            "note": f"ObeyX should verify and decide"
        }
        thermal_log.append(report)

        print(f"[ThermalAI] 🔥 High {component} usage: {value}")
        print(f"[ThermalAI] ⚠️ Suggested action: {action}")

        # إرسال التقرير لـ ObeyX
        try:
            from obeyx_core.obeyx_interface import obeyx_thermal_alert
            obeyx_thermal_alert(report)
        except ImportError:
            print("⚠️ ObeyX interface not ready")

def thermal_watchdog():
    while True:
        components = {
            "CPU": get_cpu_temp(),
            "GPU": get_gpu_temp(),
            "RAM": get_ram_usage(),
            "BATTERY": get_battery_temp()
        }

        for comp, val in components.items():
            if val is not None:
                smart_react(comp, val)

        fans = get_fan_status()
        if fans:
            print("[ThermalAI] 🌀 Fans status:", fans)

        time.sleep(5)  # كل 5 ثواني

# نقطة التشغيل
def start_thermal_controller():
    print("[ThermalAI] 🌡️ Smart thermal controller started...")
    t = threading.Thread(target=thermal_watchdog)
    t.daemon = True
    t.start()
