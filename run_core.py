import subprocess
import sys
import os

# الوحدات المتوفرة داخل ai_core
modules = {
    "analyzer": "ai_core.analyzer.analyzer",
    "generator": "ai_core.generator.generator",
    "dispatcher": "ai_core.dispatcher.dispatcher",
    "voice": "ai_core.voice.voice",
    "commands": "ai_core.commands.commands"
}

def run_module(name):
    if name not in modules:
        print(f"\n[❌] الوحدة '{name}' غير موجودة.")
        return

    module_path = modules[name]
    print(f"\n[🚀] تشغيل الوحدة: {name} ({module_path})\n")
    subprocess.run([sys.executable, "-m", module_path])

def interactive_mode():
    print("\n🧠 اختر وحدة لتشغيلها:\n")
    for i, key in enumerate(modules, 1):
        print(f"{i}. {key}")
    
    choice = input("\n🔢 رقم الوحدة > ")
    try:
        index = int(choice) - 1
        module_name = list(modules.keys())[index]
        run_module(module_name)
    except:
        print("\n[⚠️] اختيار غير صالح، أعد المحاولة.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        interactive_mode()
    else:
        run_module(sys.argv[1])
