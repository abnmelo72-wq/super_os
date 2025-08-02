import json
import os

CONFIG_PATH = "/etc/super_os/config.json"

class BootConfig:
    def __init__(self, path=CONFIG_PATH):
        self.path = path
        self.config = self.load()

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    return json.load(f)
            except:
                return self.default_config()
        return self.default_config()

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w') as f:
            json.dump(self.config, f, indent=4)

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

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()

    def reset(self):
        self.config = self.default_config()
        self.save()
