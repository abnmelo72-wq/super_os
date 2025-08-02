import psutil
import time
import datetime
import json
import os
import threading
import random

class FutureFailurePredictor:
    def __init__(self):
        self.history = []
        self.alert_level = 0
        self.model_trained = False
        self.load_previous_state()

    def load_previous_state(self):
        try:
            if os.path.exists("prediction/logs.json"):
                with open("prediction/logs.json", "r") as f:
                    self.history = json.load(f)
                    self.model_trained = True
        except Exception as e:
            print(f"[PREDICTOR] Failed to load logs: {e}")

    def save_state(self):
        try:
            with open("prediction/logs.json", "w") as f:
                json.dump(self.history, f)
        except Exception as e:
            print(f"[PREDICTOR] Failed to save logs: {e}")

    def collect_data(self):
        return {
            "timestamp": str(datetime.datetime.now()),
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "temp": self.get_temperature(),
            "disk": psutil.disk_usage('/').percent,
            "net": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv,
        }

    def get_temperature(self):
        try:
            temps = psutil.sensors_temperatures()
            for name, entries in temps.items():
                for entry in entries:
                    return entry.current
        except:
            return random.randint(30, 85)  # fallback fake temp

    def analyze_risk(self, data):
        risk = 0
        if data["cpu"] > 90: risk += 1
        if data["ram"] > 85: risk += 1
        if data["disk"] > 90: risk += 1
        if data["temp"] > 80: risk += 1
        if data["net"] > 10**9: risk += 1
        return risk

    def notify_obeyx(self, level, data):
        if level >= 2:
            print(f"[🔥 ALERT to ObeyX] Risk level {level} detected!")
            print(f"→ Suggestion: Reduce performance mode or delay high-load tasks.")
            print(f"→ Data snapshot: {json.dumps(data, indent=2)}")
        else:
            print(f"[✓ OK] System operating within safe limits.")

    def run(self):
        print("[PREDICTOR] Starting Future Failure Prediction Engine...")
        while True:
            data = self.collect_data()
            risk = self.analyze_risk(data)
            self.history.append(data)
            self.save_state()
            self.notify_obeyx(risk, data)
            time.sleep(10)  # interval between checks

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()
