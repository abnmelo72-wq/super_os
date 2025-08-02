#!/usr/bin/env python3
import os
import sys

def check_venv():
    # التحقق من تشغيل venv
    if sys.prefix == sys.base_prefix:
        print("❌ يجب تشغيل هذا السكربت داخل venv.")
        sys.exit(1)

def welcome():
    print("🔮 مرحبًا بك في المساعد الذكي داخل نظام super_os")
    print("🧠 جارٍ تحميل الوحدات...")

def main():
    check_venv()
    welcome()
    # لاحقًا: تحميل modules وربطها
    # مثال:
    # from ai_core.commands import voice_input
    # voice_input.listen()

if __name__ == "__main__":
    main()
# ... محتوى main.py السابق ...

# تشغيل وحدة الأوامر
from ai_core.commands.command_engine import run_command_engine

run_command_engine()
