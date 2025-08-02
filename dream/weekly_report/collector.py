import os
import datetime

UNITS_PATH = os.path.expanduser("~/super_os/")

# الوحدات التي سيتم تحليل نشاطها
UNITS = ["ai_core/analyzer", "ai_core/generator", "ai_core/commands", "ai_core/dispatcher", "ai_core/voice"]

def collect_activity():
    report_lines = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    report_lines.append(f"# تقرير نشاط أسبوعي - {now}\n")

    for unit in UNITS:
        path = os.path.join(UNITS_PATH, unit)
        if os.path.exists(path):
            modified_files = []
            for root, dirs, files in os.walk(path):
                for f in files:
                    full_path = os.path.join(root, f)
                    mtime = os.path.getmtime(full_path)
                    last_modified = datetime.datetime.fromtimestamp(mtime)
                    if (datetime.datetime.now() - last_modified).days <= 7:
                        modified_files.append(full_path.replace(UNITS_PATH, ""))
            if modified_files:
                report_lines.append(f"🧠 وحدة: {unit.split('/')[-1]}")
                for file in modified_files:
                    report_lines.append(f"   - تم تعديله: {file}")
                report_lines.append("")
    return "\n".join(report_lines)
