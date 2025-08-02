from datetime import datetime, timedelta

def get_week_dates():
    today = datetime.now()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def gather_report_data():
    # لاحقًا بنربطه بالنظام الحقيقي
    return {
        "week_start": get_week_dates()[0],
        "week_end": get_week_dates()[1],
        "commands_executed": 123,
        "top_commands": "فتح الكاميرا، تصفح الملفات، حل مشكلة البطارية",
        "voice_commands": 83,
        "text_commands": 40,
        "issues_fixed": "- مشكلة حرارة المعالج\n- ضعف اتصال الواي فاي",
        "system_updates": "- تحديث محرك الصوت\n- تحسين استجابة الذكاء الصناعي",
        "user_notes": "- تجربة ممتازة خلال هذا الأسبوع",
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
