import os
import subprocess

# قائمة أوامر مدعومة كبداية
command_map = {
    "افتح المتصفح": "firefox",
    "افتح الطرفية": "gnome-terminal",
    "اعد التشغيل": "reboot",
    "اطفئ الجهاز": "shutdown now",
    "حدث النظام": "apt update && apt upgrade -y"
}

def execute_command(text):
    matched = None

    for phrase, cmd in command_map.items():
        if phrase in text:
            matched = cmd
            break

    if matched:
        print(f"🚀 تنفيذ الأمر: {matched}")
        try:
            subprocess.run(matched, shell=True)
        except Exception as e:
            print(f"[❌] خطأ أثناء التنفيذ: {e}")
    else:
        print("🤔 لم أتعرف على الأمر. سيتم تمريره لاحقًا للذكاء الاصطناعي.")
