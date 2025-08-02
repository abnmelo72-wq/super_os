#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ObeyX Boot Core - init/main.py
نظام الإقلاع المتكامل لتهيئة ObeyX
"""

import os
import sys
import time
import logging
import platform
import subprocess

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

class ObeyXBoot:
    def __init__(self):
        self.boot_stage = "Starting"
        self.boot_data = {}

    def log(self, message):
        logging.info(f"[BOOT] {message}")

    def check_venv(self):
        if sys.prefix == sys.base_prefix:
            self.log("⚠️ لم يتم تفعيل البيئة الافتراضية، سيتم تفعيلها تلقائيًا...")
            subprocess.call("source ~/super_os/venv-super/bin/activate", shell=True)
            time.sleep(1)

    def check_proot(self):
        if "ANDROID_ROOT" not in os.environ:
            self.log("❌ لم يتم الكشف عن بيئة Proot. تأكد من تشغيل النظام ضمن Debian عبر proot.")
            sys.exit(1)

    def show_logo(self):
        os.system("clear")
        print(r"""
 ██████╗  ██████╗ ███████╗██╗   ██╗██╗  ██╗
██╔═══██╗██╔════╝ ██╔════╝██║   ██║╚██╗██╔╝
██║   ██║██║  ███╗█████╗  ██║   ██║ ╚███╔╝ 
██║   ██║██║   ██║██╔══╝  ██║   ██║ ██╔██╗ 
╚██████╔╝╚██████╔╝██║     ╚██████╔╝██╔╝ ██╗
 ╚═════╝  ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝
         🧠 ObeyX Boot System v1.0
""")

    def system_info(self):
        print(f"📟 النظام: {platform.system()} {platform.release()}")
        print(f"🧠 المعالج: {platform.processor()}")
        print(f"🗂️ مجلد العمل: {os.getcwd()}")
        print(f"⏱️ الوقت: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    def load_components(self):
        self.log("⚙️ تحميل مكونات النظام الأساسية...")
        # مستقبلاً: load modules like AI, audio, interface
        time.sleep(1)
        self.log("✔️ تم تحميل جميع الوحدات الأساسية.")

    def launch_obeyx(self):
        self.log("🚀 إطلاق المساعد الذكي ObeyX...")
        time.sleep(1)
        os.system("python3 ../obeyx_core/obeyx_main.py")

    def start_sequence(self):
        self.check_proot()
        self.check_venv()
        self.show_logo()
        self.system_info()
        self.load_components()
        self.launch_obeyx()
        self.log("✅ تم إنهاء تسلسل الإقلاع.")

if __name__ == "__main__":
    boot = ObeyXBoot()
    boot.start_sequence()
