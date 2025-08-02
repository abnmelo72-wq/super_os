import json
import os
import time
import hashlib
from datetime import datetime

CONFIG_BASE_PATH = "/etc/super_os/configs/"
DEFAULT_USER = "default"
ENCODED_KEYS = ["password", "api_key"]  # مفاتيح سيتم تشفيرها إن وجدت

class SmartBootConfig:
    def __init__(self, user=DEFAULT_USER):
        self.user = user
        self.path = os.path.join(CONFIG_BASE_PATH, f"{user}.json")
        self.backup_path = self.path + ".bak"
        self.log_path = self.path + ".log"
        self.last_checksum = ""
        self.config = self.load()

    def default_config(self):
        return {
            "language": "auto",
            "debug": False,
            "safe_mode": False,
            "features": {
                "ai_assist": True,
                "voice": False,
                "logging": True
            }
        }

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    config = json.load(f)
                    self.last_checksum = self._checksum(config)
                    return config
            except Exception as e:
                print(f"⚠️ فشل التحميل: {e}, استخدام الإعدادات الافتراضية.")
        return self.default_config()

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._validate_config()
        self._backup()
        self._log_change()
        with open(self.path, 'w') as f:
            json.dump(self.config, f, indent=4)
        self.last_checksum = self._checksum(self.config)

    def set(self, key, value):
        if key in ENCODED_KEYS:
            value = self._encode(value)
        self.config[key] = value
        self.save()

    def get(self, key, default=None):
        val = self.config.get(key, default)
        if key in ENCODED_KEYS and isinstance(val, str):
            return self._decode(val)
        return val

    def reset(self):
        self.config = self.default_config()
        self.save()

    def _checksum(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def _validate_config(self):
        if not isinstance(self.config, dict):
            raise ValueError("❌ تنسيق الإعدادات غير صالح.")
        if "features" not in self.config:
            self.config["features"] = {}

    def _backup(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as original, open(self.backup_path, 'w') as backup:
                backup.write(original.read())

    def _log_change(self):
        now = datetime.now().isoformat()
        with open(self.log_path, 'a') as log:
            log.write(f"[{now}] Config updated.\n")

    def _encode(self, value):
        return value[::-1]  # تشفير بسيط مؤقت: عكس السلسلة

    def _decode(self, value):
        return value[::-1]

    def auto_reload_if_changed(self):
        """يعيد تحميل الإعدادات إذا تغيّر الملف خارجيًا"""
        if not os.path.exists(self.path):
            return
        with open(self.path) as f:
            data = json.load(f)
            current_checksum = self._checksum(data)
            if current_checksum != self.last_checksum:
                print("🔄 تم الكشف عن تغيير في الإعدادات، إعادة التحميل...")
                self.config = data
                self.last_checksum = current_checksum
