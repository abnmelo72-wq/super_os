import re

def analyze_command(command):
    """
    يحلل الأمر المُدخل من المستخدم ويُصنفه حسب النية العامة (Intent).
    """
    command = command.lower().strip()

    if not command:
        return {"intent": "empty", "details": ""}

    # intent: launch app
    if any(word in command for word in ["افتح", "شغل", "ابدأ", "run", "open", "launch"]):
        return {"intent": "launch_app", "details": command}

    # intent: request info
    if any(word in command for word in ["ما هو", "من هو", "define", "what is", "who is", "اشرح", "شرح"]):
        return {"intent": "info_request", "details": command}

    # intent: calculation (numerical)
    if re.match(r'^\s*\d+\s*[\+\-\*/]\s*\d+\s*$', command) or any(word in command for word in ["احسب", "كم", "calculate", "نسبة", "ناتج"]):
        return {"intent": "calculate", "details": command}

    # intent: communication
    if any(word in command for word in ["ارسل", "قل", "اكتب", "send", "say", "write", "message"]):
        return {"intent": "communicate", "details": command}

    # intent: exit
    if any(word in command for word in ["أغلق", "اقفل", "stop", "exit", "terminate", "خروج", "انهاء"]):
        return {"intent": "close_app", "details": command}

    return {"intent": "unknown", "details": command}
