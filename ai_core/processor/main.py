# super_os/ai_core/processor/main.py

def process_input(user_input: str) -> dict:
    """
    تحليل مدخل المستخدم وتحديد النوع والإجراء المناسب.
    """
    result = {
        "type": "unknown",
        "intent": None,
        "target_module": None,
        "confidence": 0.0,
        "text": user_input
    }

    user_input = user_input.strip().lower()

    # أوامر صوتية
    if user_input.startswith("شغل") or user_input.startswith("افتح"):
        result["type"] = "command"
        result["intent"] = "launch_app"
        result["target_module"] = "commands"
        result["confidence"] = 0.95

    # أسئلة
    elif user_input.endswith("?") or "ما هو" in user_input or "شو يعني" in user_input:
        result["type"] = "question"
        result["intent"] = "get_info"
        result["target_module"] = "analyzer"
        result["confidence"] = 0.9

    # حوار طبيعي
    elif any(x in user_input for x in ["كيفك", "مرحبا", "شلونك", "صباح الخير"]):
        result["type"] = "conversation"
        result["intent"] = "greeting"
        result["target_module"] = "generator"
        result["confidence"] = 0.9

    else:
        result["type"] = "conversation"
        result["intent"] = "unknown"
        result["target_module"] = "generator"
        result["confidence"] = 0.5

    return result
