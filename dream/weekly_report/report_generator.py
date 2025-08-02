import os
from report_data import gather_report_data

def generate_report():
    with open("report_template.txt", "r", encoding="utf-8") as template:
        content = template.read()

    data = gather_report_data()

    for key, value in data.items():
        content = content.replace(f"{{{key}}}", str(value))

    filename = f"weekly_report_{data['week_start']}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[✓] تم إنشاء التقرير: {filename}")
