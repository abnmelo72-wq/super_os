import os
import uuid
import json
import socket
import datetime
import platform
import shutil
import getpass

SESSION_FILE_DEFAULT = "/tmp/super_os_session.json"
SESSION_FILE_BACKUP = os.path.expanduser("~/.super_os/session.json")

class SuperSession:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.datetime.now().isoformat()
        self.hostname = socket.gethostname()
        self.username = getpass.getuser()
        self.env = dict(os.environ)
        self.network = self.get_network_info()
        self.flags = self.analyze_environment()

        self.data = {
            "session_id": self.session_id,
            "hostname": self.hostname,
            "username": self.username,
            "start_time": self.start_time,
            "env": self.env,
            "network": self.network,
            "flags": self.flags,
        }

    def get_network_info(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())
            gateway = os.popen("ip route | grep default | awk '{print $3}'").read().strip()
            dns = os.popen("cat /etc/resolv.conf | grep nameserver | awk '{print $2}'").read().strip()
            return {"ip": ip, "gateway": gateway, "dns": dns}
        except Exception:
            return {"ip": "unknown", "gateway": "unknown", "dns": "unknown"}

    def analyze_environment(self):
        return {
            "is_root": os.geteuid() == 0 if hasattr(os, 'geteuid') else False,
            "inside_proot": 'PROOT_TMP_DIR' in os.environ,
            "inside_docker": os.path.exists('/.dockerenv'),
            "inside_venv": (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)),
        }

    def save(self, path=SESSION_FILE_DEFAULT):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def backup(self):
        self.save(SESSION_FILE_BACKUP)

    def load(self, path=SESSION_FILE_DEFAULT):
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.data = json.load(f)
                self.session_id = self.data.get("session_id", self.session_id)
        return self.data

    def update_env(self):
        self.env = dict(os.environ)
        self.data["env"] = self.env
        self.save()

    def get_summary(self):
        return {
            "session": self.session_id,
            "host": self.hostname,
            "user": self.username,
            "root": self.flags["is_root"],
            "venv": self.flags["inside_venv"],
            "proot": self.flags["inside_proot"],
            "ip": self.network["ip"],
            "start": self.start_time
        }

    def print_summary(self):
        summary = self.get_summary()
        print(json.dumps(summary, indent=4))
