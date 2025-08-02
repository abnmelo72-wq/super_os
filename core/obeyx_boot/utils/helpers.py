# utils/helpers.py

def print_banner():
    print("="*50)
    print("        ⚙️  ObeyX Boot Utility Module ⚙️")
    print("="*50)

def safe_import(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False
