import os
import psutil
import time
import threading
from datetime import datetime

# 🧠 قاعدة بيانات لتعليم ObeyX
energy_logs = []

# أوضاع الطاقة
POWER_MODES = {
    "eco": {"cpu_percent_limit": 30, "disable_cores": True, "fan_boost": False},
    "balanced": {"cpu_percent_limit": 60, "disable_cores": False, "fan_boost": False},
    "performance": {"cpu_percent_limit": 95, "disable_cores": False, "fan_boost": True},
    "emergency_cooldown": {"cpu_percent_limit": 15, "disable_cores": True, "fan_boost": True}
}

current_mode = "balanced"
SIMULATION_MODE = False  # لتجربة النظام بدون تأثيرات حقيقية

def get_temp():
    try:
        temps = psutil.sensors_temperatures()
        for name in temps:
            if "cpu" in name.lower() or "coretemp" in name.lower():
                return temps[name][0].current
        return None
    except:
        return None

def get_battery_level():
    battery = psutil.sensors_battery()
    return battery.percent if battery else None

def log_energy_state():
    entry = {
        "timestamp": datetime.now().isoformat(),
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "temp": get_temp(),
        "battery": get_battery_level()
    }
    energy_logs.append(entry)
    if len(energy_logs) > 500:
        energy_logs.pop(0)

def auto_optimize():
    high_cpu_count = sum(1 for e in energy_logs if e["cpu"] > 90)
    avg_temp = sum(e["temp"] or 0 for e in energy_logs if e["temp"]) / max(1, sum(1 for e in energy_logs if e["temp"]))
    last_temps = [e["temp"] for e in energy_logs[-5:] if e["temp"]]
    temp_surge = False
    if len(last_temps) >= 2 and (last_temps[-1] - last_temps[0]) > 15:
        temp_surge = True

    battery = get_battery_level()
    if temp_surge:
        return "emergency_cooldown"
    if battery and battery < 20:
        return "eco"
    if high_cpu_count > 100 and avg_temp > 75:
        return "eco"
    elif avg_temp < 50 and high_cpu_count < 30:
        return "performance"
    else:
        return "balanced"

def notify_user(msg):
    print(f"[🔔] {msg}")
    try:
        os.system(f'notify-send "ObeyX PowerOptimizer" "{msg}"')
    except:
        pass

def apply_power_mode(mode):
    global current_mode
    if mode == current_mode:
        return
    current_mode = mode
    config = POWER_MODES[mode]
    
    print(f"[⚡] Switching to {mode.upper()} mode | CPU Limit: {config['cpu_percent_limit']}%")

    if not SIMULATION_MODE:
        if config["disable_cores"]:
            print("🔻 Deactivating idle CPU cores.")
        if config["fan_boost"]:
            print("🌀 Boosting system fans.")

    notify_user(f"Power mode changed to: {mode.upper()}")

def monitor_power():
    while True:
        log_energy_state()
        optimized_mode = auto_optimize()
        apply_power_mode(optimized_mode)
        time.sleep(5)

def set_mode_manually(mode):
    if mode in POWER_MODES:
        apply_power_mode(mode)
    else:
        print(f"🚫 Unknown mode: {mode}")

def get_status():
    return {
        "mode": current_mode,
        "cpu_usage": psutil.cpu_percent(),
        "ram_usage": psutil.virtual_memory().percent,
        "temperature": get_temp(),
        "battery": get_battery_level()
    }

def boot_power_optimizer(simulate=False):
    global SIMULATION_MODE
    SIMULATION_MODE = simulate
    print("[🧠] ObeyX PowerOptimizer Booting...")
    if SIMULATION_MODE:
        print("⚠️ Running in SIMULATION mode. No real changes will be made.")
    threading.Thread(target=monitor_power, daemon=True).start()

# 🧪 تجربة
if __name__ == "__main__":
    boot_power_optimizer(simulate=False)
    while True:
        print(get_status())
        time.sleep(10)
