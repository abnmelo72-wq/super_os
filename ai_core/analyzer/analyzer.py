#!/usr/bin/env python3
import os
import json
import sys

# تحقق من أننا داخل venv
if sys.prefix == sys.base_prefix:
    print("❌ يجب تشغيل هذا السكربت داخل بيئة افتراضية (venv).")
    sys.exit(1)

# أوامر بسيطة للتصنيف اليدوي المبدئي
DOMAINS = {
    "system": ["shutdown", "reboot", "battery", "cpu", "ram", "temperature", "status", "sysinfo"],
    "internet": ["search", "google", "open website", "wikipedia", "download"],
    "media": ["play", "pause", "music", "video", "volume", "mute"],
    "apps": ["launch", "open", "start", "run"],
    "ai": ["summarize", "translate", "explain", "write", "code", "fix", "generate"],
    "tools": ["calculator", "notepad", "camera", "screenshot"],
    "personal": ["my name", "profile", "who am i", "calendar", "reminder"]
}

def classify(text):
    text = text.lower()
    detected = {"domain": "unknown", "intent": None, "raw": text}

    for domain, keywords in DOMAINS.items():
        for keyword in keywords:
            if keyword in text:
                detected["domain"] = domain
                detected["intent"] = keyword
                return detected

    return detected

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️  استخدام: python analyze.py 'نص الأمر'")
        sys.exit(1)

    input_text = sys.argv[1]
    result = classify(input_text)
    print(json.dumps(result, indent=4))
